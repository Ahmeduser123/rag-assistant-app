from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    """Happy path: /health should return 200 and a status field."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_query_happy_path():
    """Happy path: a valid question should return a 200 with an answer and sources."""
    response = client.post("/query", json={"question": "What is the recommended dosage of metformin for adults?"})
    assert response.status_code == 200

    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0

    assert "sources" in data
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0
    assert "drug" in data["sources"][0]
    assert "section" in data["sources"][0]


def test_query_invalid_input():
    """Invalid input: an empty question should be rejected with 422."""
    response = client.post("/query", json={"question": ""})
    assert response.status_code == 422