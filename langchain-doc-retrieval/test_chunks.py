from src.core.document_processor import DocumentProcessor
processor = DocumentProcessor()
docs = processor.load_directory("./data/documents")
chunks = processor.split_documents(docs)
for i, c in enumerate(chunks):
    print(f"--- Chunk {i} ---")
    print(c.page_content[:200])
