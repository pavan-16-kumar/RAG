from fastapi import APIRouter, HTTPException, Depends
from src.api.models import IngestRequest, IngestResponse, QueryRequest, QueryResponse
from src.services.ingestion import IngestionService
from src.services.qa import QAService
from src.utils.logger import logger

router = APIRouter()

# Dependency Injection for Services
def get_ingestion_service():
    return IngestionService()

def get_qa_service():
    return QAService()

@router.get("/health", response_model=dict, tags=["System"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "service": "LangChain Document Retrieval API"}

@router.post("/ingest", response_model=IngestResponse, tags=["Document Processing"])
def ingest_documents(
    request: IngestRequest,
    service: IngestionService = Depends(get_ingestion_service)
):
    """
    Ingests all supported documents from the provided directory path.
    Chunks them using the core logic and pushes embeddings into ChromaDB.
    """
    logger.info(f"API Request to /ingest with path: {request.directory_path}")
    result = service.ingest_directory(request.directory_path)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return IngestResponse(**result)

@router.post("/query", response_model=QueryResponse, tags=["QA Pipeline"])
def query_documents(
    request: QueryRequest,
    service: QAService = Depends(get_qa_service)
):
    """
    Queries the vector database using the RAG pipeline.
    Combines retrieved contexts with the prompt to generate an answer.
    """
    logger.info(f"API Request to /query with question: {request.question}")
    result = service.ask_question(request.question)
    
    if result.get("error"):
        logger.error(f"Error serving query: {result['error']}")
        # Using 500 as this indicates a failure in retrieval/llm rather than user error
        raise HTTPException(status_code=500, detail="Error generating answer.")
        
    return QueryResponse(answer=result["answer"], sources=result["sources"])
