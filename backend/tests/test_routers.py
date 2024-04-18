from fastapi.testclient import TestClient

from main import app  # replace with the path to your FastAPI app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Add more tests for each endpoint...
