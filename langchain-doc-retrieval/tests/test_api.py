from fastapi.testclient import TestClient
from src.api.main import app
import pytest

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "service" in response.json()

# Given these depend heavily on having a valid DB and OpenRouter key, 
# you'd ideally mock the services here.
# For industry readiness, this demonstrates the testing entrypoints.

@pytest.fixture
def mock_ingest(monkeypatch):
    class MockService:
        def ingest_directory(self, path):
            return {"status": "success", "message": "Mocked", "chunks_added": 5}
            
    monkeypatch.setattr("src.api.routes.get_ingestion_service", lambda: MockService())

def test_ingest_mocked(mock_ingest):
    response = client.post("/ingest", json={"directory_path": "./dummy"})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Mocked", "chunks_added": 5}
