import threading
from sentence_transformers import SentenceTransformer
from app.config import settings

class EmbeddingService:
    def __init__(self):
        self._model = None
        self._lock = threading.Lock()

    @property
    def model(self):
        if self._model is None:
            with self._lock:
                if self._model is None:
                    self._model = SentenceTransformer(settings.EMBEDDING_MODEL)
        return self._model

    def encode(self, texts):
        return self.model.encode(texts, normalize_embeddings=True,
                                 convert_to_numpy=True)
