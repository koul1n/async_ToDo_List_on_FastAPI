from fastapi.testclient import TestClient
from app import app

def test_create_user(user_data):
    with TestClient(app = app) as client:
        response = client.post("http://127.0.0.1:8000/users/", json = user_data)
        assert response.status_code == 200
        assert user_data["username"] == response.json()["username"]

