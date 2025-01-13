from fastapi import FastAPI
from app.users.users_routes import router as user_router
from app.tasks.tasks_routes import router as task_router
from app.database import database_helper, database_for_test
import os


app = FastAPI()



if os.getenv("TESTING"):  # Проверяем переменную окружения
    app.dependency_overrides[database_helper.get_db] = database_for_test.get_db

app.include_router(task_router, tags=["tasks"], prefix='/api/v1')
app.include_router(user_router, tags=["users"], prefix='/api/v1')


