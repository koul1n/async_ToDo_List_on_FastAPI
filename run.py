from fastapi import FastAPI
import uvicorn
from app.users import router as user_router
from app.tasks import router as task_router

host = '127.0.0.1'
port = 8000

app = FastAPI()

app.include_router(task_router)
app.include_router(user_router)


if __name__ == '__main__':
    uvicorn.run(app, host = host, port = port)