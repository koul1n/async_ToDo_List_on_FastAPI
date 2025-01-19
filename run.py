"""
Этот файл содержит точку входа для запуска приложения с использованием Uvicorn.

Он настраивает сервер, используя параметры хоста и порта из конфигурации. Также добавлено логирование ошибок при запуске сервера.
"""

import uvicorn
from app.logs import logger
from app import app
from app.database import settings
import sys
from uuid import uuid4


if __name__ == "__main__":
    """
    Запуск приложения с использованием Uvicorn.

    Если сервер не удается запустить, ошибка будет залогирована, и процесс завершится с кодом 1.
    """
    try:
        uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
    except Exception as ex:
        logger.bind(log_id = str(uuid4())).error(f"Error starting the server: {ex}")
        sys.exit(settings.EXIT_CODE_ERROR)
