import pytest
import pytest_asyncio
from faker import Faker
from datetime import datetime, timedelta
from httpx import AsyncClient
from fastapi import status

faker = Faker()

@pytest.fixture
def user_data():
    data = {
        "username": faker.user_name(),
        "email": faker.email(domain="gmail.com"),
        "password": faker.password()
    }
    return data

@pytest.fixture
def task_data():
    data = {
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=100),
        "deadline": (datetime.now() + timedelta(days=faker.random_int(min=1, max=10))).isoformat()
    }
    return data


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient() as async_client:
        yield async_client


@pytest_asyncio.fixture
async def auth_token(async_client, user_data):
    user_data_for_login = {
        "username" : user_data['email'],
        "password" : user_data['password']
    }
    # Создаем пользователя (или логинимся) и получаем токен
    response = await async_client.post("http://127.0.0.1:8000/users/login/", json=user_data_for_login)
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    return response_json["access_token"]  # Предполагаем, что токен хранится в "access_token"
