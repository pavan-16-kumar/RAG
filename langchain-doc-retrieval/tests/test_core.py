import pytest
from src.core.document_processor import DocumentProcessor
from langchain_core.documents import Document

def test_document_processor_initialization():
    processor = DocumentProcessor()
    assert processor is not None
    assert processor.text_splitter.chunk_size == 1000  # Default from settings
    
def test_split_documents():
    processor = DocumentProcessor()
    docs = [Document(page_content="This is a test document. " * 100)]
    chunks = processor.split_documents(docs)
    
    # Should be at least 2 chunks because 100 * len("This is a test document. ") > 1000
    assert len(chunks) > 1
    assert len(chunks[0].page_content) <= 1000
