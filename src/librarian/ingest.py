import chromadb
import os
import requests

DB_PATH = "src/librarian/chroma_db"
COLLECTION_NAME = "wiseclaw_memory"

class OllamaEmbeddingFunction:
    def __init__(self, model_name="nomic-embed-text"):
        self.model_name = model_name

    def __call__(self, input):
        if isinstance(input, str): input = [input]
        embeddings = []
        for text in input:
            res = requests.post(
                "http://localhost:11434/api/embeddings",
                json={"model": self.model_name, "prompt": text}
            )
            embeddings.append(res.json()["embedding"])
        return embeddings

def ingest_text(text, metadata=None):
    client = chromadb.PersistentClient(path=DB_PATH)
    embedding_func = OllamaEmbeddingFunction()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_func
    )

    collection.add(
        documents=[text],
        metadatas=[metadata] if metadata else [{}],
        ids=[str(os.urandom(8).hex())]
    )
    return "Documento ingerido com sucesso via Soberania Local."
