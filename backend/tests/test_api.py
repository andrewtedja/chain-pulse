from fastapi.testclient import TestClient
from app.services import app

client = TestClient(app)

def test_get_news():
    response = client.get("/api/news")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)