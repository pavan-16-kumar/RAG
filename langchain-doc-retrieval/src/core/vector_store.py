from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from src.core.embeddings import EmbeddingProvider
from src.config.settings import settings
from src.utils.logger import logger

class VectorStoreManager:
    """Manages adding documents to and querying the Vector Database."""
    
    def __init__(self):
        self.embedding = EmbeddingProvider.get_embeddings()
        self.persist_directory = settings.chroma_persist_directory
        self.collection_name = settings.collection_name
        self.vector_store = self._init_vector_store()
        
    def _init_vector_store(self) -> Chroma:
        """Initializes or loads the localized ChromaDB instance."""
        logger.info(f"Initializing Chroma VectorStore at {self.persist_directory}")
        return Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding,
            persist_directory=self.persist_directory
        )
        
    def add_documents(self, documents: List[Document]) -> None:
        """Embeds and adds documents to the vector store."""
        if not documents:
            logger.warning("No documents provided to add_documents.")
            return
            
        try:
            self.vector_store.add_documents(documents)
            self.vector_store.persist()
            logger.info(f"Successfully added and persisted {len(documents)} document chunks to ChromaDB.")
        except Exception as e:
            logger.error(f"Failed to add documents to VectorStore: {str(e)}")
            raise
            
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Performs a similarity search using the vector store."""
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Retrieved {len(docs)} documents for query: '{query}'")
            return docs
        except Exception as e:
            logger.error(f"Similarity search failed: {str(e)}")
            return []
            
    def as_retriever(self, search_kwargs: dict = {"k": 4}):
        """Returns the vector store as a LangChain BaseRetriever."""
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)
