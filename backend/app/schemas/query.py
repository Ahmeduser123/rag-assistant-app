from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Incoming request body for POST /query."""
    question: str = Field(..., min_length=1, description="The user's question about a drug.")


class SourceReference(BaseModel):
    """A single source the answer was grounded in."""
    drug: str
    section: str


class QueryResponse(BaseModel):
    """Response body for POST /query."""
    answer: str
    sources: list[SourceReference]