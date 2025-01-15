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
