from fastapi import APIRouter

from app.schemas.query import QueryRequest, QueryResponse, SourceReference
from app.services.retrieval import retrieve
from app.services.generation import generate_answer

router = APIRouter()


@router.get("/health")
def health_check():
    """Simple liveness check — confirms the API is up and reachable."""
    return {"status": "ok"}


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    """
    Full RAG flow: retrieve relevant chunks for the question, generate a
    grounded answer from them, and return both the answer and the sources
    actually used (independent of what the LLM claims it cited).
    """
    retrieved_chunks = retrieve(request.question)
    answer = generate_answer(request.question, retrieved_chunks)

    sources = [
        SourceReference(drug=chunk["drug"], section=chunk["section"])
        for chunk in retrieved_chunks
    ]

    return QueryResponse(answer=answer, sources=sources)