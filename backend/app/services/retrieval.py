from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from app.core.config import settings

# Loaded once at import time (module-level), not per-request — this is
# what makes retrieval fast: no re-loading the embedding model or
# reconnecting to the vector store on every question.
_model = SentenceTransformer(settings.embedding_model_name)
_client = chromadb.PersistentClient(path=settings.vector_store_dir)
_collection = _client.get_or_create_collection(name=settings.collection_name)

_known_drugs = sorted(
    set(_collection.get()["metadatas"][i]["drug"] for i in range(_collection.count()))
)


def embed_query(question: str) -> list[float]:
    """Embeds a question with the same prefix convention used at index time."""
    prefixed = f"{settings.query_prefix}{question}"
    return _model.encode(prefixed, convert_to_numpy=True).tolist()


def detect_drug_in_question(question: str) -> str | None:
    """Checks if the question names one of the known drugs (case-insensitive)."""
    q_lower = question.lower()
    for drug in _known_drugs:
        drug_readable = drug.replace("_", " ")
        if drug_readable in q_lower or drug in q_lower:
            return drug
    return None


def retrieve(question: str, top_k: int | None = None) -> list[dict]:
    """
    Retrieves the top_k most relevant chunks for a question, hard-filtered
    to the named drug when one is detected in the question (prevents
    cross-drug retrieval contamination between similarly-worded labels).
    """
    top_k = top_k or settings.top_k
    query_embedding = embed_query(question)
    detected_drug = detect_drug_in_question(question)

    query_kwargs = {"query_embeddings": [query_embedding], "n_results": top_k}
    if detected_drug:
        query_kwargs["where"] = {"drug": detected_drug}

    results = _collection.query(**query_kwargs)

    retrieved = []
    for i in range(len(results["ids"][0])):
        retrieved.append({
            "text": results["documents"][0][i],
            "drug": results["metadatas"][0][i]["drug"],
            "section": results["metadatas"][0][i]["section"],
            "distance": results["distances"][0][i],
        })
    return retrieved