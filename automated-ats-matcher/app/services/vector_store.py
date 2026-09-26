import uuid
from pathlib import Path
import chromadb
from app.config import settings

class VectorStore:
    def __init__(self, embeddings):
        Path(settings.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
        self.embeddings = embeddings
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self.collection = self.client.get_or_create_collection(
            name="ats_documents", metadata={"hnsw:space": "cosine"})

    def similarity(self, resume, jd):
        vectors = self.embeddings.encode([resume, jd])
        return max(0.0, min(1.0, float(vectors[0] @ vectors[1])))

    def index_resume(self, filename, text):
        vector = self.embeddings.encode([text])[0].tolist()
        self.collection.upsert(
            ids=[str(uuid.uuid4())], embeddings=[vector], documents=[text],
            metadatas=[{"filename": filename, "type": "resume"}])
