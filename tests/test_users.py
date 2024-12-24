from fastapi.testclient import TestClient
import pytest
from unittest.mock import MagicMock
from app import app
from app.models import User

@pytest.fixture
def user_data():
    data = {
        "username" : "test_username",
        "password" : "test_password",
        "email" : "test@gmail.com"
    }
    return data

@pytest.fixture
def mock_get_db():
    mock_db = MagicMock()
    yield mock_db

@pytest.mark.asyncio
async def create_user(user_data):
    async with TestClient(app = app) as client:
        response = await client.post("/users/", json = user_data)
        assert response.status_code == 200
        response_json = response.json()
        assert all(response_json[check] == user_data[check] for check in ["username", "email"])




