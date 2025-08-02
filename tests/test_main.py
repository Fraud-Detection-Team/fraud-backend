from fastapi.testclient import TestClient
from app.main import app  # adjust import if app is your root

client = TestClient(app)

def test_root_path_returns_404():
    response = client.get("/")
    assert response.status_code == 404  # since no root path is defined

