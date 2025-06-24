# llms/load_llm.py

import os
from typing import Any

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq


def load_llm(model_name: str) -> Any:
    """
    Dynamically load the appropriate LLM client based on the model name.
    """
    model_name = model_name.lower()

    if model_name.startswith("gpt") or model_name.startswith("openai"):
        print("Using OpenAI model:", model_name)
        return ChatOpenAI(
            temperature=0,
            model_name=model_name,  # use exact model name like "gpt-4o"
            openai_api_key=os.environ.get("AUTH_TOKEN")
        )

    elif model_name.startswith("gemini"):
        print("Using Google Gemini model:", model_name)
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0,
            google_api_key=os.environ.get("GOOGLE_API_KEY")
        )

    elif model_name.startswith(("groq", "llama", "mistral", "deepseek")):
        print("Using Groq-based model:", model_name)
        return ChatGroq(
            groq_api_key=os.environ.get("GROQ_API_KEY"),
            model_name=model_name
        )
    
    else:
        raise ValueError(f"Unsupported model name: {model_name}")
