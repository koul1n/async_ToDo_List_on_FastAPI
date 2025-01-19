"""
Этот файл содержит конфигурацию приложения FastAPI, включая настройку middleware для логирования,
а также настройку жизненного цикла приложения.
"""

import os
from fastapi import FastAPI
from app.logs import log_middleware, logger
from app.database import database_for_test, database_helper
from app.tasks.tasks_routes import router as task_router
from app.users.users_routes import router as user_router
from uuid import uuid4
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_helper.log_id = str(uuid4())
    try:
        if os.getenv("TESTING", None):
            app.dependency_overrides[database_helper.get_db] = database_for_test.get_db
            await database_for_test.test_connection()
        else:
            await database_helper.test_connection()
        yield
    except Exception as e:
        logger.bind(log_id=database_helper.log_id).error(
            f"Lifespan startup failed: {str(e)}"
        )
        raise e


app = FastAPI(lifespan=lifespan)

app.middleware("http")(log_middleware)


app.include_router(task_router, tags=["tasks"])
app.include_router(user_router, tags=["users"])
