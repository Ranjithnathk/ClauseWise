# Use official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install system dependencies + Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean

# Copy the entire project (ignores things listed in .dockerignore)
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Expose Streamlit port (optional, if using single container)
EXPOSE 8501

# Set default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
