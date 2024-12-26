import pytest
from faker import Faker
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app import app
from app.database import database_helper, database_for_test

faker = Faker()


@pytest.fixture
def user_data():
    data = {
        "username" : faker.user_name(),
        "email" : faker.email(domain="gmail.com"),
        "password" : faker.password()
    }
    return data

@pytest.fixture
def task_data():
    data = {
        "title" : faker.sentence(nb_words=5),
        "description" : faker.text(max_nb_chars=100),
        "deadline" : datetime.now() + timedelta(days=faker.random_int(min = 1, max = 10))
    }
    return data

@pytest.fixture(scope="function")
def client():
    # Переопределяем зависимость FastAPI на тестовую базу данных
    app.dependency_overrides[database_helper.get_db] = database_for_test.get_db
    with TestClient(app) as client:
        yield client



