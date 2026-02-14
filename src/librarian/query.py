
import sys
import os
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings

WORK_DIR = "/a0/usr/workdir"
DB_PATH = os.path.join(WORK_DIR, "src/librarian/chroma_db")
COLLECTION_NAME = "librarian_docs"

def query(text, limit=3):
    print(f"[LIBRARIAN] Querying for: '{text}'...")
    try:
        client = chromadb.PersistentClient(path=DB_PATH)
        collection = client.get_collection(name=COLLECTION_NAME)

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        query_vector = embeddings.embed_query(text)

        results = collection.query(
            query_embeddings=[query_vector],
            n_results=limit
        )

        print(f"\n[RESULTS]")
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i]
                dist = results['distances'][0][i] if results['distances'] else 0
                source = os.path.basename(meta.get('source', 'unknown'))
                page = meta.get('page', '?')
                # Simple replace for preview
                preview = doc[:150].replace('\n', ' ')
                print(f"- [Dist: {dist:.4f}] {preview}... (Source: {source}, Page: {page})")
        else:
            print("No results found.")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query(sys.argv[1])
    else:
        print("Usage: python query.py 'your question'")
