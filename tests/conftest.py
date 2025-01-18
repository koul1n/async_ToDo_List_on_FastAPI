"""
Тестовые фикстуры для настройки данных и клиента в асинхронных тестах.

Описание:
Этот модуль предоставляет фикстуры для использования в тестах Pytest, включая создание данных
для пользователей и задач, а также настройку асинхронного HTTP-клиента.

Фикстуры:
1. **user_data**:
   - Генерирует тестовые данные для пользователя с использованием библиотеки `Faker`.
   - Данные включают: имя пользователя, email и пароль.

2. **task_data**:
   - Генерирует тестовые данные для задачи с использованием `Faker`.
   - Данные включают: заголовок, описание и срок выполнения (deadline).

3. **async_client**:
   - Предоставляет асинхронный HTTP-клиент `AsyncClient` для выполнения запросов.
   - Область действия: `function` (создается новый клиент для каждого теста).

Использование:
- Подключите фикстуры к тестам, указав их в параметрах тестовой функции.
"""

from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from faker import Faker
from httpx import AsyncClient

faker = Faker()


@pytest.fixture
def user_data():
    data = {
        "username": faker.user_name(),
        "email": faker.email(domain="gmail.com"),
        "password": faker.password(),
    }
    return data


@pytest.fixture
def task_data():
    data = {
        "title": faker.sentence(nb_words=5),
        "description": faker.text(max_nb_chars=100),
        "deadline": (
            datetime.now() + timedelta(days=faker.random_int(min=1, max=10))
        ).isoformat(),
    }
    return data


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient() as async_client:
        yield async_client
