from fastapi import FastAPI
import uvicorn
from app.routes import router as task_router

host = '127.0.0.1'
port = 8000

app = FastAPI()

app.include_router(task_router)

if __name__ == '__main__':
    uvicorn.run(app, host = host, port = port)