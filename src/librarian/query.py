import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
import os

COLLECTION_NAME = "wiseclaw_memory"
CHROMA_PATH = "/a0/usr/workdir/src/librarian/chroma_db"

class FixedOllamaEF(OllamaEmbeddingFunction):
    def name(self):
        return "ollama"

def query_memory(prompt, n_results=3):
    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        embedding_func = FixedOllamaEF(
            model_name="nomic-embed-text",
            url="http://localhost:11434/api/embeddings"
        )

        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_func
        )

        results = collection.query(
            query_texts=[prompt],
            n_results=n_results
        )

        if results and 'documents' in results and results['documents']:
            return results['documents'][0]
    except Exception as e:
        print(f"Librarian Error: {e}")
    return []