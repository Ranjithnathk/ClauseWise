import os
from typing import List
from langchain.docstore.document import Document
from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def load_file(file_path: str) -> List[Document]:
    """
    Load documents from a file based on its extension.
    Supports PDF, TXT, CSV, DOC, DOCX.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    elif ext == ".csv":
        loader = CSVLoader(file_path)
    elif ext in [".doc", ".docx"]:
        loader = UnstructuredWordDocumentLoader(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return loader.load()


def parse_and_chunk(file_paths: List[str], username: str = None) -> List[Document]:
    """
    Load all files, combine documents, and split into chunks.
    Returns a list of Document chunks.
    If username is provided, documents are assumed to be under uploaded_docs/{username}/
    """
    all_docs = []
    for file_path in file_paths:
        try:
            # Adjust file path if user-specific
            if username and username.lower() != "public":
                file_path = os.path.join(UPLOAD_DIR, username, os.path.basename(file_path))
            docs = load_file(file_path)
            all_docs.extend(docs)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(all_docs)

    print(f"🔍 Total chunks created: {len(chunks)}")
    for i, chunk in enumerate(chunks[:3]):
        print(f"Chunk {i + 1}:\n{chunk.page_content}\n")

    return chunks
