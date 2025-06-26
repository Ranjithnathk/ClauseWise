# ClauseWise Intelligent Legal Document Assistant (RAG + Multi-LLM)
## Your AI Attorney to clear your Legal doubts

![Build](https://img.shields.io/github/actions/workflow/status/Ranjithnathk/ClauseWise/backend.yml?label=backend%20CI&logo=github)  
![Python](https://img.shields.io/badge/python-3.10-blue.svg) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg)

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