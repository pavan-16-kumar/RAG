# LangChain Document Retrieval System

Welcome to the **LangChain Document Retrieval System**! This is an industry-ready, scalable project designed to process, store, and intelligently retrieve information from various document formats using Retrieval-Augmented Generation (RAG).

## 🚀 Features

- **Multi-format Support**: Ingest PDF, DOCX, TXT, HTML, and Markdown files.
- **Advanced RAG Pipeline**: Leverages LangChain for semantic chunking and embedding.
- **Vector Database Integration**: Uses state-of-the-art vector stores (Chroma) for fast similarity search.
- **LLM-Powered Q&A**: Employs OpenRouter to access various models (like GPT-4) to synthesize answers with accurate citations.
- **Dual Interfaces**: Interact via a powerful REST API (FastAPI) or a convenient Command Line Interface (CLI).
- **Production Ready**: Includes proper logging, error handling, configuration management, and Docker support.

## 📚 Documentation

The project includes thorough documentation to help you get started and understand the architecture:

- [QUICKSTART](QUICKSTART.md): Get up and running in 5 minutes.
- [ARCHITECTURE](ARCHITECTURE.md): Deep dive into system design and data flows.
- [PROJECT_SUMMARY](PROJECT_SUMMARY.md): Overview and goals.
- [COMPLETE_FOLDER_STRUCTURE](COMPLETE_FOLDER_STRUCTURE.md): Detailed breakdown of every file.
- [IMPLEMENTATION_GUIDE](IMPLEMENTATION_GUIDE.md): Code examples and usage instructions.

## 🛠️ Tech Stack

- **Frameworks**: LangChain, FastAPI, Typer
- **LLMs & Embeddings**: OpenRouter / OpenAI Compatible
- **Vector Store**: Chroma
- **Language**: Python 3.10+
- **Deployment**: Docker & Docker Compose
