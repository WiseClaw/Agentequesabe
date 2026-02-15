
import chromadb
from chromadb.utils import embedding_functions
import os

class Librarian:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="src/librarian/chroma_db")
        self.collection = None
        self.embedding_func = None

    def _get_collection(self):
        if self.collection:
            return self.collection

        # Lazy load embedding function
        if not self.embedding_func:
            print("[LIBRARIAN] Loading embedding model (this may take a moment)...")
            try:
                self.embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
            except Exception as e:
                print(f"[LIBRARIAN ERROR] Failed to load embeddings: {e}")
                return None

        self.collection = self.client.get_or_create_collection(
            name="wiseclaw_memory",
            embedding_function=self.embedding_func
        )
        return self.collection

    def query(self, query_text, n_results=3):
        collection = self._get_collection()
        if not collection:
            return "[MEMORY ERROR] Database unavailable."

        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []
