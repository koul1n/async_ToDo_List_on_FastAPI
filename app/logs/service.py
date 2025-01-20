"""
Этот файл содержит middleware для логирования запросов и ответов в приложении FastAPI.
Он автоматически записывает информацию о запросах, включая путь запроса, статус ответа,
а также обрабатывает ошибки и исключения, логируя их с соответствующими уровнями.

Основные компоненты:
    - log_middleware: Middleware, которое логирует информацию о запросах и ответах, включая ошибки.

    Логирование:
        - Для успешных запросов (коды 200-299) записывается информация о пути запроса и статусе ответа.
        - Для неудачных запросов (коды 401, 403, 404) записывается предупреждение.
        - В случае ошибки записывается информация о неудачном запросе с подробным описанием ошибки.

"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger
from uuid import uuid4
from typing import Callable

logger.remove()
logger.add(
    "app.log",
    level="INFO",
    rotation="1 MB",
    retention="7 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {extra[log_id]} | {message}",
)


async def log_middleware(request: Request, call_next: Callable):
    """
    Middleware для логирования запросов и ответов.

    Параметры:
        request (Request): Объект запроса FastAPI.
        call_next (callable): Функция для вызова следующего обработчика запроса.

    Возвращаемое значение:
        Response: Ответ от обработчика запроса.

    Логирует:
        - Информацию о пути запроса и статусе ответа.
        - Предупреждения для ошибок 401, 403 и 404.
        - Ошибки, если запрос завершился исключением.
    """
    log_id = str(uuid4())
    try:
        response = await call_next(request)

        if response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]:
            logger.bind(log_id=log_id).warning(
                f"Request to {request.url.path} failed with status {response.status_code}"
            )
        else:
            logger.bind(log_id=log_id).info(
                f"Successfully accessed {request.url.path} with status {response.status_code}"
            )

    except Exception as ex:
        logger.bind(log_id=log_id).error(f"Request to {request.url.path} failed: {ex}")
        response = JSONResponse(
            content={"success": False, "error": str(ex)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
