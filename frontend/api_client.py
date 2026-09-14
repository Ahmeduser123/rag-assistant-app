import os

import requests
from dotenv import load_dotenv

load_dotenv()  # reads .env and sets its values as environment variables

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def query_backend(question: str) -> dict:
    """
    Sends a question to the backend's /query endpoint and returns the
    parsed JSON response ({"answer": ..., "sources": [...]}).
    Raises an exception on network failure or non-200 response, which
    the calling UI code is responsible for catching and displaying nicely.
    """
    response = requests.post(
        f"{API_BASE_URL}/query",
        json={"question": question},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()