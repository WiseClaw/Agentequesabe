
import os
from glob import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
from uuid import uuid4

# Configuration
WORK_DIR = "/a0/usr/workdir"
SOURCE_DIR = os.path.join(WORK_DIR, "pesquisas")
DB_PATH = os.path.join(WORK_DIR, "src/librarian/chroma_db")
COLLECTION_NAME = "librarian_docs"

def ingest():
    print(f"[LIBRARIAN] Starting ingestion from {SOURCE_DIR}...")

    # 1. Setup ChromaDB
    client = chromadb.PersistentClient(path=DB_PATH)
    # Delete if exists to start fresh (optional, good for testing)
    try:
        client.delete_collection(COLLECTION_NAME)
        print("[LIBRARIAN] Cleared existing collection.")
    except Exception as e:
        print(f"[LIBRARIAN] Collection did not exist or could not be deleted: {e}")

    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    # 2. Setup Embeddings (Local - Save Tokens)
    print("[LIBRARIAN] Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 3. Load Documents
    pdf_files = glob(os.path.join(SOURCE_DIR, "*.pdf"))
    all_splits = []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )

    for file_path in pdf_files:
        print(f"[LIBRARIAN] Processing {os.path.basename(file_path)}...")
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        splits = text_splitter.split_documents(docs)
        all_splits.extend(splits)

    print(f"[LIBRARIAN] Created {len(all_splits)} chunks. Embedding and storing...")

    # 4. Embed and Store in Batches
    batch_size = 100
    total_batches = (len(all_splits) + batch_size - 1) // batch_size

    for i in range(0, len(all_splits), batch_size):
        batch = all_splits[i:i+batch_size]
        print(f"[LIBRARIAN] Processing batch {i//batch_size + 1}/{total_batches}...")

        ids = [str(uuid4()) for _ in batch]
        documents = [doc.page_content for doc in batch]
        metadatas = [{
            "source": doc.metadata.get("source", "unknown"),
            "page": doc.metadata.get("page", 0)
        } for doc in batch]

        # Generate embeddings
        embeddings_list = embeddings.embed_documents(documents)

        collection.add(
            ids=ids,
            embeddings=embeddings_list,
            documents=documents,
            metadatas=metadatas
        )

    print(f"[LIBRARIAN] Successfully stored {len(all_splits)} chunks in {DB_PATH}.")

if __name__ == "__main__":
    ingest()
