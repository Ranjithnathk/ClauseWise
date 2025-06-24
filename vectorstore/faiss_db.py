# vectorstore/faiss_db.py

import os
from typing import List, Optional
from langchain_community.vectorstores import FAISS  # updated import per latest recommendations
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)


def save_to_faiss(docs: List[Document], username: str, pdf_name: str) -> None:
    """
    Save documents to a FAISS index specific to a user and PDF.

    - Public docs (username == "public") saved in vectorstore/faiss_indexes/
    - User docs saved in vectorstore/faiss_indexes/<username>/
    """
    if username == "public":
        index_path = os.path.join("vectorstore", "faiss_indexes", pdf_name)
    else:
        index_path = os.path.join("vectorstore", "faiss_indexes", username, pdf_name)

    os.makedirs(index_path, exist_ok=True)
    vectorstore = FAISS.from_documents(docs, embedding_model)
    vectorstore.save_local(index_path)
    print(f"FAISS index saved at: {index_path}")


def load_faiss_index(username: Optional[str], pdf_name: str) -> Optional[FAISS]:
    """
    Load the FAISS index specific to a user and PDF.

    - Public docs (username None or "public") loaded from vectorstore/faiss_indexes/
    - User docs loaded from vectorstore/faiss_indexes/<username>/
    """
    if username in [None, "public"]:
        index_path = os.path.join("vectorstore", "faiss_indexes", pdf_name)
    else:
        index_path = os.path.join("vectorstore", "faiss_indexes", username, pdf_name)

    if not os.path.exists(index_path):
        print(f"FAISS index path '{index_path}' does not exist.")
        return None

    return FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
