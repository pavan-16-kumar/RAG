import os
import shutil
from src.core.document_processor import DocumentProcessor
from src.core.vector_store import VectorStoreManager
from src.utils.logger import logger

class IngestionService:
    """Service layer orchestrating document ingestion."""
    
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.vector_store_manager = VectorStoreManager()
        
    def ingest_directory(self, directory_path: str) -> dict:
        """
        Loads all documents from a directory, chunks them, and adds them to the vector store.
        """
        logger.info(f"Starting ingestion process for directory: {directory_path}")
        
        # 1. Load documents
        raw_documents = self.doc_processor.load_directory(directory_path)
        if not raw_documents:
            logger.warning(f"No documents loaded from {directory_path}. Aborting ingestion.")
            return {"status": "error", "message": "No valid documents found.", "chunks_added": 0}
            
        # 2. Chunk documents
        chunked_documents = self.doc_processor.split_documents(raw_documents)
        
        # 3. Add to vector store
        try:
            self.vector_store_manager.add_documents(chunked_documents)
            return {
                "status": "success",
                "message": f"Successfully ingested {len(raw_documents)} documents.",
                "chunks_added": len(chunked_documents)
            }
        except Exception as e:
            logger.error(f"Ingestion failed during vector storage: {str(e)}")
            return {"status": "error", "message": str(e), "chunks_added": 0}

    def reset_vector_store(self, persist_dir: str):
        """DANGER: Completely removes the existing vector store database."""
        if os.path.exists(persist_dir):
            try:
                shutil.rmtree(persist_dir)
                logger.info(f"Deleted vector store at {persist_dir}")
                # Re-initialize vector store manager
                self.vector_store_manager = VectorStoreManager()
                return {"status": "success", "message": "Vector store reset."}
            except Exception as e:
                logger.error(f"Failed to delete vector store: {str(e)}")
                return {"status": "error", "message": str(e)}
        return {"status": "success", "message": "Vector store directory does not exist, nothing to reset."}
