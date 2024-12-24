from fastapi import FastAPI
from app.users import router as user_router
from app.tasks import router as task_router


app = FastAPI()

app.include_router(task_router, tags=['tasks'])
app.include_router(user_router, tags = ['users'])
