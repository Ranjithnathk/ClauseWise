# ClauseWise - Full Stack Multi-LLM RAG Assistant
## Your AI Attorney to clear your Legal doubts

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://gemini.google.com/)
[![LLaMA 3](https://img.shields.io/badge/LLaMA3-0054B1?style=for-the-badge&logo=meta&logoColor=white)](https://ai.meta.com/llama/)
[![Mistral](https://img.shields.io/badge/Mistral-4B0082?style=for-the-badge&logo=wind&logoColor=white)](https://mistral.ai/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-1B1B1B?style=for-the-badge&logo=deepnote&logoColor=white)](https://deepseek.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-000000?style=for-the-badge&logo=chainlink&logoColor=white)](https://www.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![FAISS](https://img.shields.io/badge/FAISS-2C7BB6?style=for-the-badge&logo=apache&logoColor=white)](https://github.com/facebookresearch/faiss)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/)
[![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-CA504F?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-AEC0D6?style=for-the-badge&logo=github&logoColor=black)](https://en.wikipedia.org/wiki/CI/CD)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## Live Demo

**Frontend (Streamlit App)**  
 [https://clausewise-frontend.run.app](https://clausewise-frontend-140738413424.us-central1.run.app)

**Backend (FastAPI API)**  
 [https://clausewise-backend.run.app](https://clausewise-backend-140738413424.us-central1.run.app)

---

## Features

- Upload & parse legal PDFs  
- Multi-LLM support: `GPT-4o`, `Gemini-2.0-flash`, `Llama3-70b-8192`, `Mistral-saba-24b`,`Deepseek-r1-distill-llama-70b`
- Real-time legal question answering  
- Citation-backed RAG responses  
- Login / Signup authentication   
- FAISS vector store for document retrieval  
- Dockerized frontend + backend  
- CI/CD via GitHub Actions  
- GCP Cloud Run deployment

---

## Tech Stack

| Layer       | Stack                                  |
|-------------|----------------------------------------|
| Frontend    | Streamlit                              |
| Backend     | FastAPI                                |
| LLMs        | OpenAI, Gemini, Mistral, LLaMA, DeepSeek |
| Vector DB   | FAISS                                  |
| DevOps      | Docker, GitHub Actions, GCP Cloud Run  |
| Auth        | JWT, SQLAlchemy                        |

---

## Folder Structure

```
ClauseWise/
├── .github/
│   └── workflows/
│       ├── backend.yml
│       └── frontend.yml
├── database/
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── database.py
├── llms/
│   └── load_llm.py
├── parsers/
│   └── file_parser.py
├── vectorstore/
│   ├── faiss_db.py
│   └── faiss_indexes/
├── uploaded_docs/
├── ui/
│   └── ui.py
├── build_faiss_indexes.py
├── evaluate_rag.py
├── main.py
├── Dockerfile
├── Dockerfile.streamlit
├── requirements.txt
├── evaluation_data.json
├── README.md
└── .env

```

---

## Local Development


### 1. Clone the repo
```bash
git clone https://github.com/Ranjithnathk/ClauseWise.git && cd ClauseWise
```

### 2. Create & activate virtual environment
```
conda create -p venv python==3.10 -y 
source activate venv/
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Create a .env file in the root directory 
```
OPENAI_API_KEY = "your_openai_api_key"
GROQ_API_KEY = "your_groq_api_key"
TAVILY_API_KEY = "your_tavily_api_key"
GOOGLE_API_KEY = "your_google_api_key"
JWT_SECRET_KEY = "your_jwt_secret_key"
AUTH_TOKEN = "your_auth_token"
```

### 5. Run Backend
```
uvicorn main:app --reload --port 8000
```

### 6. Run Frontend
```
streamlit run ui/ui.py
```

---

## Docker (Frontend + Backend)
**Backend**
```
docker build -t clausewise-backend -f Dockerfile .
docker run -p 8000:8000 clausewise-backend
```

**Frontend**
```
docker build -t clausewise-frontend -f Dockerfile.streamlit .
docker run -p 8501:8501 clausewise-frontend
```

---

## GCP Cloud Run Deployment

### Backend
```
docker build -t gcr.io/YOUR_PROJECT_ID/clausewise-backend .
docker push gcr.io/YOUR_PROJECT_ID/clausewise-backend
gcloud run deploy clausewise-backend --image gcr.io/YOUR_PROJECT_ID/clausewise-backend --platform managed --region us-central1 --allow-unauthenticated
```

### Frontend
```
docker build -t gcr.io/YOUR_PROJECT_ID/clausewise-frontend -f Dockerfile.streamlit .
docker push gcr.io/YOUR_PROJECT_ID/clausewise-frontend
gcloud run deploy clausewise-frontend --image gcr.io/YOUR_PROJECT_ID/clausewise-frontend --platform managed --region us-central1 --allow-unauthenticated
```

---

## Future Enhancements

- Multi-document comparison agent
- Clause-level extraction & explanation
- Document upload via URLs
- Role-based access ( Admin, Reviewer)
- Long context window support ( GPT-4-128k)

---

## License

This project is licensed under the MIT License.

---

## Author

Done by [Ranjithnath Karunanidhi](https://www.linkedin.com/in/ranjithnathk/)