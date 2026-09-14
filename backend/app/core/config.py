from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central app settings, loaded from environment variables / a .env file.
    Keeping these here (instead of hardcoded across the codebase) means
    changing a model name or path never requires touching business logic.
    """

    # Vector store
    vector_store_dir: str = "data/vector_store"
    collection_name: str = "drug_leaflets"

    # Embedding model — MUST match what the notebook used to build the
    # vector store, or retrieval quality silently degrades.
    embedding_model_name: str = "BAAI/bge-base-en-v1.5"
    query_prefix: str = "query: "
    passage_prefix: str = "passage: "

    # Ollama / generation
    ollama_model: str = "llama3.2:3b"
    top_k: int = 5

    # CORS — the frontend's origin, so the browser allows requests through
    frontend_origin: str = "http://localhost:8501"  # default Streamlit port

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()