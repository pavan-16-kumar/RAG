# ⚡ Quickstart Guide

Get the LangChain Document Retrieval System running on your local machine in under 5 minutes.

## Prerequisites

- Python 3.10+
- **OpenRouter API Key**

## 1. Setup Environment

```bash
# Clone or navigate to the project directory
cd langchain-doc-retrieval

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## 2. Configuration

Copy the example environment file and add your credentials:

```bash
cp .env.example .env
```

Open `.env` and set your `OPENROUTER_API_KEY`:

```
OPENROUTER_API_KEY=your_actual_api_key_here
```

## 3. Ingest Documents

Place some text, PDF, or markdown files into the `data/documents` folder. Then run the CLI ingestion command:

```bash
# Ingest all documents in the folder
python -m src.ui.cli ingest --path ./data/documents
```

## 4. Query the System

Use the CLI to ask a question based on the ingested documents:

```bash
python -m src.ui.cli query -q "What are the main topics discussed in the documents?"
```

## 5. Run the REST API

Alternatively, you can start the FastAPI server:

```bash
uvicorn src.api.main:app --reload
```

- Visit **http://localhost:8000/docs** to see the interactive API documentation.
- You can now send POST requests to `/ingest` and `/query`.
