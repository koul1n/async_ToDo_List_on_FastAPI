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
                "Request to %s failed with status %d", request.url.path, response.status_code
            )
        else:
            logger.bind(log_id=log_id).info(
                "Successfully accessed %s with status %d", request.url.path, response.status_code
            )

    except Exception as ex:
        logger.bind(log_id=log_id).error("Request to %s failed: %s", request.url.path, ex)
        response = JSONResponse(
            content={"success": False, "error": str(ex)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
