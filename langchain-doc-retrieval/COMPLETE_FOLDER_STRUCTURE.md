# 🌳 Complete Folder Structure

This document provides a detailed, file-by-file explanation of the LangChain Document Retrieval project structure.

## 📂 Root Directory: `langchain-doc-retrieval/`

### 📄 Documentation (8 files)

- 📁 **README.md** - Main documentation, introduction, features, and high-level setup.
- 📁 **QUICKSTART.md** - A 5-minute setup guide to get the project running immediately.
- 📁 **ARCHITECTURE.md** - Detailed system design, data flow diagrams, and component interactions.
- 📁 **PROJECT_SUMMARY.md** - High-level overview of the project's goals, scope, and deliverables.
- 📁 **COMPLETE_FOLDER_STRUCTURE.md** - This file. A visual tree with detailed descriptions of every file.
- 📁 **IMPLEMENTATION_GUIDE.md** - Step-by-step usage examples, code snippets, and API usage.
- 📁 **TREE_STRUCTURE.txt** - Raw file tree output for quick reference.

### 📁 `src/` - Source Code

The core logic of the application, structured following Domain-Driven Design (DDD) principles.

#### 📁 `src/config/` - Settings & Prompts

- 📄 `settings.py` - Centralized Pydantic models for managing environment variables and application configurations.
- 📄 `prompts.py` - Standardized LLM prompts for different tasks (Q&A, summarization, etc.).

#### 📁 `src/core/` - Core System Components

- 📄 `document_processor.py` - Logic for loading and chunking documents of various formats (PDF, DOCX, TXT, HTML, MD).
- 📄 `embeddings.py` - Wrapper for embedding models (e.g., OpenAIEmbeddings, HuggingFaceEmbeddings).
- 📄 `vector_store.py` - Abstraction over vector databases (ChromaDB, FAISS, Pinecone) for storing and retrieving chunks.

#### 📁 `src/services/` - Business Logic

- 📄 `ingestion.py` - Orchestrates the process of reading files -> processing -> embedding -> storing.
- 📄 `retrieval.py` - Logic for semantic search, hybrid search, and filtering from the vector store.
- 📄 `qa.py` - The Retrieval-Augmented Generation (RAG) pipeline that combines retrieval with LLM generation to answer questions.

#### 📁 `src/api/` - REST API (FastAPI)

- 📄 `main.py` - FastAPI application initialization, middleware, and entry point.
- 📄 `routes.py` - API endpoints for ingestion (`/ingest`), querying (`/query`), and health checks (`/health`).
- 📄 `models.py` - Pydantic schemas for API requests and responses.

#### 📁 `src/ui/` - User Interfaces

- 📄 `cli.py` - Command-line interface using Typer or Click for local operations (ingest, query).
- 📄 `webapp.py` - (Optional) A simple Streamlit or Gradio interface for interacting with the system visually.

#### 📁 `src/utils/` - Utilities & Helpers

- 📄 `logger.py` - Configured logging utility for consistent log formats and levels.
- 📄 `helpers.py` - Common utility functions, file system operations, validation logic.

### 📁 `tests/` - Test Suite

- 📄 `test_core.py` - Unit tests for core components (document processor, embeddings).
- 📄 `test_services.py` - Integration tests for ingestion and Q&A pipelines.
- 📄 `test_api.py` - API endpoint tests using FastAPI TestClient.

### 📁 `data/` - Runtime Data

- 📁 `documents/` - Directory for placing raw files (PDFs, TXT) to be ingested.
- 📁 `indexes/` - Local storage for vector databases (e.g., ChromaDB persistence directory).
- 📁 `logs/` - Application log files.

### 📁 `docker/` - Containerization

- 📄 `Dockerfile` - Instructions to build the application image.
- 📄 `docker-compose.yml` - Multi-container setup (API + maybe a separate DB container).

### 📁 Sub-folders & Scripts

- 📁 `scripts/` - Shell scripts for automation (e.g., `setup.sh`, `run_tests.sh`).
- 📁 `notebooks/` - Jupyter notebooks for EDA, prototyping, and evaluating retrieval metrics.

### 📄 Configuration Files

- 📄 `requirements.txt` - Python dependencies.
- 📄 `.env.example` - Template for required environment variables.
- 📄 `.gitignore` - Standard git ignore definitions.
