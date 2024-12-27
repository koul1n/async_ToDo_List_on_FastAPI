import pytest
import pytest_asyncio
from faker import Faker
from datetime import datetime, timedelta
from httpx import AsyncClient

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
        "deadline": datetime.now() + timedelta(days=faker.random_int(min=1, max=10))
    }
    return data


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient() as async_client:
        yield async_client
