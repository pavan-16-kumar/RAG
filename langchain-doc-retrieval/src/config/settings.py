import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Application settings, loaded from environment variables or .env file."""
    
    # App config
    app_name: str = "LangChain Document Retrieval"
    app_env: str = "development"
    app_debug: bool = True
    
    # OpenRouter config
    openrouter_api_key: Optional[str] = None
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model_name: str = "openai/gpt-4-turbo"
    openrouter_embedding_model: str = "openai/text-embedding-3-small"
    
    # Vector store config
    chroma_persist_directory: str = "./data/indexes/chroma"
    collection_name: str = "document_retrieval_collection"
    
    # Document processing config
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate settings singleton
settings = Settings()

# Ensure necessary directories exist
os.makedirs(settings.chroma_persist_directory, exist_ok=True)
os.makedirs("./data/documents", exist_ok=True)
os.makedirs("./data/logs", exist_ok=True)
