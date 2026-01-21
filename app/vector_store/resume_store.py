import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.utils.data_loader import load_all_documents
from pathlib import Path

RESUME_VECTOR_PATH = "vector_store_resume"
RESUME_COLLECTION = "resume_documents"

_embedding = None
_resume_db = None


def get_embedding():
    global _embedding
    if _embedding is None:
        _embedding = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
    return _embedding


def get_resume_retriever(k: int = 3):
    global _resume_db
    print("🔥 Initializing Resume Retriever")

    if _resume_db is not None:
        return _resume_db.as_retriever(search_kwargs={"k": k})

    documents = load_all_documents(Path("data/resumes"))
    if not documents:
        print("⚠️ No resume documents found")
        return None

    os.makedirs(RESUME_VECTOR_PATH, exist_ok=True)

    _resume_db = Chroma(
        persist_directory=RESUME_VECTOR_PATH,
        collection_name=RESUME_COLLECTION,
        embedding_function=get_embedding(),
    )

    if _resume_db._collection.count() == 0:
        _resume_db.add_documents(documents)
        print("✅ Resume documents indexed")

    return _resume_db.as_retriever(search_kwargs={"k": k})

