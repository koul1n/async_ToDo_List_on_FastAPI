import uvicorn
from app import app

host = '127.0.0.1'

port = 8000

if __name__ == '__main__':
    uvicorn.run(app, host = host, port = port)