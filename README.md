# ClauseWise Intelligent Legal Document Assistant (RAG + Multi-LLM)
## Your AI Attorney to clear your Legal doubts

![Build](https://img.shields.io/github/actions/workflow/status/Ranjithnathk/ClauseWise/backend.yml?label=backend%20CI&logo=github)  

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

![License](https://img.shields.io/badge/license-MIT-green.svg)


[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://gemini.google.com/)
[![LLaMA 3](https://img.shields.io/badge/LLaMA3-0054B1?style=for-the-badge&logo=meta&logoColor=white)](https://ai.meta.com/llama/)
[![Mistral](https://img.shields.io/badge/Mistral-A6C48A?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjRkZGIiB2aWV3Qm94PSIwIDAgNjQgNjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTMyIDY0QzE0LjM0IDY0IDAgNDkuNjYgMCAzMiAwIDE0LjM0IDE0LjM0IDAgMzIgMGMxNy42NCAwIDMyIDE0LjM0IDMyIDMyIDAgMTcuNjQtMTQuMzYgMzItMzIgMzJ6Ii8+PC9zdmc+)](https://www.mistral.ai/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-1B1B1B?style=for-the-badge&logo=deepnote&logoColor=white)](https://deepseek.com/)


[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-000000?style=for-the-badge&logo=chainlink&logoColor=white)](https://www.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![FAISS](https://img.shields.io/badge/FAISS-2C7BB6?style=for-the-badge&logo=apache&logoColor=white)](https://github.com/facebookresearch/faiss)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/)
[![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)


---

## Live Demo

**Frontend (Streamlit App)**  
 [https://clausewise-frontend-xxxxx.run.app](https://clausewise-frontend-xxxxx.run.app)

**Backend (FastAPI API)**  
 [https://clausewise-backend-xxxxx.run.app](https://clausewise-backend-xxxxx.run.app)

---

## Features

- Upload & parse legal PDFs  
- Multi-LLM support: `GPT-4o`, `Gemini`, `Mistral`, `LLaMA`, `DeepSeek`, etc.  
- Real-time legal question answering  
- Citation-backed RAG responses  
- Login / Signup authentication  
- Evaluation: Faithfulness, ROUGE, BERTScore  
- FAISS vector store for document retrieval  
- Dockerized frontend + backend  
- CI/CD via GitHub Actions  
- GCP Cloud Run deployment

---

## Tech Stack

| Layer       | Stack                                  |
|-------------|----------------------------------------|
| Frontend    | [Streamlit](https://streamlit.io/)     |
| Backend     | [FastAPI](https://fastapi.tiangolo.com/) |
| LLMs        | OpenAI, Gemini, Mistral, LLaMA, DeepSeek |
| Vector DB   | [FAISS](https://faiss.ai/)             |
| DevOps      | Docker, GitHub Actions, GCP Cloud Run  |
| Auth        | JWT, SQLAlchemy                        |

---

## Folder Structure

```
ClauseWise/
├── main.py # FastAPI backend entrypoint
├── ui/ui.py # Streamlit UI
├── database/ # Auth system (JWT, models)
├── vectorstore/ # FAISS index builder & logic
├── parsers/ # File parser logic
├── llms/ # Multi-LLM orchestrator
├── Dockerfile # Backend Docker config
├── Dockerfile.streamlit # Frontend Docker config
├── requirements.txt
└── .env
```

---

## Local Development

```bash
# 1. Clone the repo
git clone https://github.com/Ranjithnathk/ClauseWise.git && cd ClauseWise

# 2. Create virtual environment
python -m venv venv && source venv/bin/activate  # (or venv\Scripts\activate on Windows)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Backend
uvicorn main:app --reload --port 8000

# 5. Run Frontend
streamlit run ui/ui.py

---

## Docker (Frontend + Backend)
Backend
docker build -t clausewise-backend -f Dockerfile .
docker run -p 8000:8000 clausewise-backend

Frontend
docker build -t clausewise-frontend -f Dockerfile.streamlit .
docker run -p 8501:8501 clausewise-frontend

---

## GCP Cloud Run Deployment

# Backend
docker build -t gcr.io/YOUR_PROJECT_ID/clausewise-backend .
docker push gcr.io/YOUR_PROJECT_ID/clausewise-backend
gcloud run deploy clausewise-backend \
  --image gcr.io/YOUR_PROJECT_ID/clausewise-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Frontend
docker build -t gcr.io/YOUR_PROJECT_ID/clausewise-frontend -f Dockerfile.streamlit .
docker push gcr.io/YOUR_PROJECT_ID/clausewise-frontend
gcloud run deploy clausewise-frontend \
  --image gcr.io/YOUR_PROJECT_ID/clausewise-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

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

Made by Ranjithnath Karunanidhi