import uvicorn
from app import app
from app.database import settings

if __name__ == '__main__':
    uvicorn.run(app, host = settings.SERVER_HOST, port = settings.SERVER_PORT)

