from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config.settings import settings
from src.utils.logger import logger

class DocumentProcessor:
    """Handles loading and chunking of documents of various formats."""
    
    LOADER_MAPPING = {
        ".pdf": PyPDFLoader,
        ".txt": TextLoader,
        ".docx": Docx2txtLoader,
        ".md": UnstructuredMarkdownLoader,
        ".html": UnstructuredHTMLLoader,
    }
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
        )
        
    def load_document(self, file_path: str) -> List[Document]:
        """Loads a single document based on its file extension."""
        ext = Path(file_path).suffix.lower()
        if ext not in self.LOADER_MAPPING:
            logger.warning(f"Unsupported file extension: {ext} for file {file_path}")
            return []
            
        try:
            loader_class = self.LOADER_MAPPING[ext]
            loader = loader_class(file_path)
            docs = loader.load()
            logger.info(f"Loaded {len(docs)} pages/sections from {file_path}")
            return docs
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            return []
            
    def load_directory(self, directory_path: str) -> List[Document]:
        """Loads all supported documents from a directory."""
        all_docs = []
        dir_path = Path(directory_path)
        
        if not dir_path.exists() or not dir_path.is_dir():
            logger.error(f"Directory not found: {directory_path}")
            return []
            
        for ext in self.LOADER_MAPPING.keys():
            for file_path in dir_path.rglob(f"*{ext}"):
                docs = self.load_document(str(file_path))
                all_docs.extend(docs)
                
        return all_docs
        
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Splits documents into smaller chunks for embedding."""
        if not documents:
            return []
            
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks
