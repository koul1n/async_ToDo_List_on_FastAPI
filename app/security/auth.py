from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.security.utils import decode_jwt

"""
Модуль для обработки аутентификации и авторизации пользователей с использованием FastAPI.

Этот модуль предоставляет функциональность для получения текущего пользователя на основе
токена OAuth2, а также проверки валидности токена с использованием JWT.
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login/")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
       Получение текущего пользователя на основе переданного токена.

       Эта функция извлекает токен из заголовка запроса, декодирует его и возвращает
       данные о пользователе. В случае невалидного или истекшего токена вызывает
       исключение HTTPException с кодом 401 (Unauthorized).
    """
    try:
        user_data = decode_jwt(token)
        return user_data
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

