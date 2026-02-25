from langchain_openai import OpenAIEmbeddings
from langchain_core.embeddings import Embeddings
from src.config.settings import settings
from src.utils.logger import logger
import os

class EmbeddingProvider:
    """Provides the embedding model used across the application."""
    
    @staticmethod
    def get_embeddings() -> Embeddings:
        """Initialize and return the configured embedding model."""
        if not settings.openrouter_api_key and not os.getenv("OPENROUTER_API_KEY"):
            logger.warning("OPENROUTER_API_KEY is not set. Embeddings will fail if requested.")
            
        try:
            return OpenAIEmbeddings(
                openai_api_key=settings.openrouter_api_key or os.getenv("OPENROUTER_API_KEY", "dummy"),
                openai_api_base=settings.openrouter_base_url,
                model=settings.openrouter_embedding_model,
                # Optionally pass kwargs like chunk_size for API limits
            )
        except Exception as e:
            logger.error(f"Failed to initialize OpenAIEmbeddings: {str(e)}")
            raise
