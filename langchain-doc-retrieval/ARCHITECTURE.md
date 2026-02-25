# 🏛️ System Architecture

This document outlines the architectural design of the LangChain Document Retrieval System.

## High-Level Architecture

The system follows a typical RAG (Retrieval-Augmented Generation) pattern, divided into two main pipelines: **Ingestion** and **Retrieval/Generation**.

```mermaid
graph TD
    A[Raw Documents] -->|Document Loaders| B(Chunking & Splitting)
    B -->|Embedding Model| C[Vector Store]
    D[User Query] -->|Embedding Model| E(Similarity Search)
    C --> E
    E -->|Retrieved Context + Query| F[LLM (e.g., GPT-4)]
    F --> G[Final Answer]
```

## Components

1.  **Core (`src/core`)**: The foundational building blocks.
    - `document_processor.py`: Uses LangChain's `UnstructuredFileLoader`, `PyPDFLoader`, etc., followed by `RecursiveCharacterTextSplitter`.
    - `embeddings.py`: Configures `OpenAIEmbeddings`.
    - `vector_store.py`: Manages the ChromaDB instance, providing abstract methods to add or query vectors.

2.  **Services (`src/services`)**: Business logic orchestration.
    - `ingestion.py`: Coordinates loading chunks from the processor, passing them to the vector store.
    - `qa.py`: Uses LangChain's `ConversationalRetrievalChain` or `create_retrieval_chain` to orchestrate sending contexts to the LLM.

3.  **API & UI (`src/api`, `src/ui`)**: Presentation layer.
    - The API maps HTTP verbs to service functions using Pydantic for validation.
    - The CLI uses Typer to provide terminal commands wrapping the same services.
