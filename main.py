import os
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
import uvicorn

# Auth & DB modules
from database import models, schemas, auth, database
from database.schemas import PDFListResponse

# Chat & PDF RAG
from llms.load_llm import load_llm
from vectorstore.faiss_db import load_faiss_index, save_to_faiss
from parsers.file_parser import parse_and_chunk
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

# --- App Initialization ---
app = FastAPI()

# --- CORS for Streamlit UI ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Mount uploaded PDFs as static folder ---
UPLOAD_FOLDER = os.path.abspath("uploaded_docs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.mount("/uploaded_docs", StaticFiles(directory=UPLOAD_FOLDER), name="uploaded_docs")

# --- DB Init ---
models.Base.metadata.create_all(bind=database.engine)

# --- Dependencies ---
def get_db():
    return next(database.get_db())

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = auth.verify_token(token)
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --- Auth Routes ---
@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# --- List PDFs (public + user-specific) ---
@app.get("/available_pdfs", response_model=PDFListResponse)
def get_available_pdfs(current_user: models.User = Depends(get_current_user)):
    username = current_user.username
    user_dir = os.path.join(UPLOAD_FOLDER, username)

    try:
        public_pdfs = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".pdf")]
        user_pdfs = [f for f in os.listdir(user_dir) if f.endswith(".pdf")] if os.path.exists(user_dir) else []
        return {"public": public_pdfs,"user": user_pdfs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing PDFs: {str(e)}")
    
    

# --- Upload PDF and build user-specific FAISS index ---
@app.post("/upload_pdf")
def upload_pdf(file: UploadFile = File(...), current_user: models.User = Depends(get_current_user)):
    try:
        username = current_user.username
        user_upload_path = os.path.join(UPLOAD_FOLDER, username)
        os.makedirs(user_upload_path, exist_ok=True)

        file_location = os.path.join(user_upload_path, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())

        docs = parse_and_chunk([file.filename], username=username)
        save_to_faiss(docs, username=username, pdf_name=os.path.splitext(file.filename)[0])
        return {"message": "PDF uploaded and indexed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload and process PDF: {str(e)}")

# --- Chat Endpoint ---
class ChatRequest(BaseModel):
    model_name: str
    messages: List[str]
    pdf_name: Optional[str] = None

DYNAMIC_RAG_PROMPT = (
    "You are a helpful assistant. Use ONLY the context provided below to answer or summarize. "
    "If the answer is not found in the document, respond with 'I could not find the answer in the documents provided.' "
    "Never use external knowledge or make assumptions."
)

@app.post("/chat")
def chat_endpoint(request: ChatRequest, current_user: models.User = Depends(get_current_user)):
    if not request.model_name or not request.pdf_name:
        raise HTTPException(status_code=400, detail="Model name and PDF name are required.")

    try:
        llm = load_llm(request.model_name)
        tools = [TavilySearchResults(max_results=2)]
        agent = create_react_agent(llm, tools)

        username = current_user.username
        pdf_name = os.path.splitext(request.pdf_name)[0]

        #vectorstore = load_faiss_index(username=username, pdf_name=pdf_name)

        user_pdf_path = os.path.join(UPLOAD_FOLDER, username, f"{pdf_name}.pdf")
        public_pdf_path = os.path.join(UPLOAD_FOLDER, f"{pdf_name}.pdf")

        if os.path.exists(user_pdf_path):
            vectorstore = load_faiss_index(username=username, pdf_name=pdf_name)
        elif os.path.exists(public_pdf_path):
            vectorstore = load_faiss_index(username="public", pdf_name=pdf_name)
        else:
            raise HTTPException(status_code=404, detail="PDF file not found.")

        if vectorstore is None:
            raise HTTPException(status_code=404, detail="FAISS index not found for this document.")

        query = request.messages[-1]
        docs = vectorstore.similarity_search(query, k=5)
        context = "\n\n".join([doc.page_content for doc in docs])

        messages = [
            {"type": "system", "content": DYNAMIC_RAG_PROMPT},
            {"type": "human", "content": f"Here is some context from your document:\n\n{context}"},
            {"type": "human", "content": query},
        ]

        state = {"messages": messages}
        result = agent.invoke(state)

        if isinstance(result, dict):
            if "output" in result:
                response = result["output"]
            elif "messages" in result and result["messages"]:
                last_msg = result["messages"][-1]
                response = getattr(last_msg, "content", str(last_msg))
            else:
                response = str(result)
        else:
            response = str(result)

        return {"answer": response}

    except Exception as e:
        import traceback
        return {"error": f"Agent execution failed: {str(e)}"}

# --- Run App ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
