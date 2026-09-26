import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

def env_float(name, default):
    try:
        return float(os.getenv(name, default))
    except ValueError:
        return float(default)

@dataclass(frozen=True)
class Settings:
    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    FLASK_HOST: str = os.getenv("FLASK_HOST", "127.0.0.1")
    FLASK_PORT: int = int(os.getenv("FLASK_PORT", "5000"))
    STREAMLIT_PORT: int = int(os.getenv("STREAMLIT_PORT", "8501"))
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    SEMANTIC_WEIGHT: float = env_float("SEMANTIC_WEIGHT", "0.50")
    LLM_WEIGHT: float = env_float("LLM_WEIGHT", "0.50")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./storage/chroma")
    MAX_UPLOAD_MB: int = int(os.getenv("MAX_UPLOAD_MB", "25"))
    MAX_ZIP_FILES: int = int(os.getenv("MAX_ZIP_FILES", "100"))
    MAX_TEXT_CHARS: int = int(os.getenv("MAX_TEXT_CHARS", "30000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
if abs(settings.SEMANTIC_WEIGHT + settings.LLM_WEIGHT - 1.0) > 0.001:
    raise ValueError("SEMANTIC_WEIGHT + LLM_WEIGHT must equal 1.0")
