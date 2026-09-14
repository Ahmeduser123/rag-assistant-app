from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes.query import router as query_router

app = FastAPI(
    title="RAG-Powered Drug Leaflet Assistant",
    description="Answers questions about drug package inserts using retrieval-augmented generation.",
    version="1.0.0",
)

# Allow the frontend's origin to call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router)