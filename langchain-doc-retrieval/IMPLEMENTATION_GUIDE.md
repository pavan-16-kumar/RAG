# 📖 Implementation Guide

This guide provides practical examples of how to interact with the LangChain Document Retrieval System.

## 1. CLI Usage

The Command-Line Interface is the easiest way to interact locally.

### Ingestion

Process all compatible files in a directory:

```bash
python -m src.ui.cli ingest --path ./data/documents
```

### Querying

Ask a question:

```bash
python -m src.ui.cli query -q "Explain the main architectural decisions."
```

## 2. API Usage (FastAPI)

Ensure the server is running: `uvicorn src.api.main:app --port 8000`

### Ingest via API

```bash
curl -X POST "http://localhost:8000/ingest" \
     -H "Content-Type: application/json" \
     -d '{"directory_path": "./data/documents"}'
```

### Query via API

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is RAG?"}'
```

## 3. Python Usage (Code Integration)

If you are importing this project as a module:

```python
from src.services.ingestion import IngestionService
from src.services.qa import QAService

# 1. Ingest Data
ingestion_service = IngestionService()
ingestion_service.ingest_directory("./data/documents")

# 2. Query Data
qa_service = QAService()
answer = qa_service.ask_question("Summarize the ingested documents.")
print(answer)
```
