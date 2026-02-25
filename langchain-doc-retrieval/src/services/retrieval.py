from typing import List
from langchain_core.documents import Document
from src.core.vector_store import VectorStoreManager
from src.utils.logger import logger

class RetrievalService:
    """Service layer for basic semantic retrieval without an active LLM completion."""
    
    def __init__(self):
        self.vector_store_manager = VectorStoreManager()
        
    def semantic_search(self, query: str, top_k: int = 4) -> List[Document]:
        """
        Retrieves the top_k most similar documents to the query from the vector store.
        """
        logger.info(f"Executing semantic search for query: '{query}'")
        try:
            results = self.vector_store_manager.similarity_search(query=query, k=top_k)
            logger.info(f"Retrieved {len(results)} chunks successfully.")
            return results
        except Exception as e:
            logger.error(f"Semantic search failed: {str(e)}")
            return []
