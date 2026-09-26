from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService
from app.services.evaluation_service import EvaluationService
from app.services.job_service import JobService

embedding_service = EmbeddingService()
vector_store = VectorStore(embedding_service)
llm_service = LLMService()
evaluation_service = EvaluationService(embedding_service, vector_store, llm_service)
job_service = JobService(evaluation_service)
