import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.utils.data_loader import load_all_documents
from pathlib import Path

POLICY_VECTOR_PATH = "vector_store_policy"
POLICY_COLLECTION = "policy_documents"

_embedding = None
_policy_db = None


def get_embedding():
    global _embedding
    if _embedding is None:
        _embedding = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
    return _embedding


def get_policy_retriever(k: int = 3):
    global _policy_db
    print("🔥 Initializing Policy Retriever")

    if _policy_db is not None:
        return _policy_db.as_retriever(search_kwargs={"k": k})

    documents = load_all_documents(Path("data/policies"))
    if not documents:
        print("⚠️ No policy documents found")
        return None

    os.makedirs(POLICY_VECTOR_PATH, exist_ok=True)

    _policy_db = Chroma(
        persist_directory=POLICY_VECTOR_PATH,
        collection_name=POLICY_COLLECTION,
        embedding_function=get_embedding(),
    )

    if _policy_db._collection.count() == 0:
        _policy_db.add_documents(documents)
        print("✅ Policy documents indexed")

    return _policy_db.as_retriever(search_kwargs={"k": k})

