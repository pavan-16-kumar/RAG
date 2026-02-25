from pydantic import BaseModel, Field
from typing import List, Optional

class IngestRequest(BaseModel):
    """Schema for ingestion requests."""
    directory_path: str = Field(
        default="./data/documents",
        title="Directory Path",
        description="The path containing files to ingest."
    )

class IngestResponse(BaseModel):
    """Schema for ingestion responses."""
    status: str
    message: str
    chunks_added: int = 0

class QueryRequest(BaseModel):
    """Schema for QA query requests."""
    question: str = Field(..., title="User Question", description="The question to ask the system.")
    
class SourceInfo(BaseModel):
    """Schema defining individual sources inside the response."""
    source: str
    page: str | int
    snippet: str

class QueryResponse(BaseModel):
    """Schema for QA query responses."""
    answer: str
    sources: List[SourceInfo] = []
    error: Optional[str] = None
