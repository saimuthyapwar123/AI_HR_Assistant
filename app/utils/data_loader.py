from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
)
from langchain_core.documents import Document

# Project root
BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "data"

LOADERS = {
    ".txt": TextLoader,
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
}


def load_all_documents(folder_path: Path | None = None) -> list[Document]:
    """
    Load documents from a specific folder.
    If no folder is provided, defaults to data/
    """

    folder = folder_path or DATA_DIR
    print(f"📁 Scanning {folder}")

    if not folder.exists():
        print(f"❌ Folder does not exist: {folder}")
        return []

    docs: list[Document] = []

    for file in folder.rglob("*"):
        if file.is_file() and file.suffix.lower() in LOADERS:
            print(f"🔹 Loading {file}")
            loader = LOADERS[file.suffix.lower()](str(file))
            loaded_docs = loader.load()

            for d in loaded_docs:
                d.metadata["source"] = str(file)

            docs.extend(loaded_docs)

    print(f"✅ Loaded {len(docs)} documents")
    return docs
