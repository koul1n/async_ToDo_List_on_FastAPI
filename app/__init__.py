"""
Этот модуль содержит основное приложение FastAPI и настраивает маршруты, а также зависимости.

Основные функции модуля:
1. Создает экземпляр приложения FastAPI.
2. Настраивает маршруты для управления задачами (`tasks_routes`) и пользователями (`users_routes`).
3. Переопределяет зависимость получения базы данных для тестирования, если установлена переменная окружения `TESTING`.

Функциональность:
- Если переменная окружения `TESTING` установлена, приложение использует тестовую базу данных, подключив зависимость `database_for_test.get_db` вместо стандартной `database_helper.get_db`.
- Маршруты:
  - `tasks`: Маршруты для работы с задачами.
  - `users`: Маршруты для управления пользователями.

Переменные:
- `app`: Экземпляр FastAPI.
"""
import os

from fastapi import FastAPI

from app.database import database_for_test, database_helper
from app.tasks.tasks_routes import router as task_router
from app.users.users_routes import router as user_router

app = FastAPI()


if os.getenv("TESTING", None):  # Проверяем переменную окружения
    app.dependency_overrides[database_helper.get_db] = database_for_test.get_db

app.include_router(task_router, tags=["tasks"])
app.include_router(user_router, tags=["users"])
