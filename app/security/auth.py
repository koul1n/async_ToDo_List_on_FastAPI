"""
Этот файл содержит функции для работы с OAuth2 и получения текущего пользователя на основе JWT-токена.
Функция `get_current_user` извлекает информацию о пользователе из токена и проверяет его действительность.

Основные компоненты:
    - oauth2_scheme: Стандартная схема аутентификации с использованием OAuth2 для извлечения токена.
    - get_current_user: Функция для получения данных текущего пользователя из JWT-токена.

    Исключения:
        - В случае неверного или истёкшего токена будет возбуждена ошибка 401 (Unauthorized).
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.security.utils import decode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login/")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Извлекает информацию о текущем пользователе из JWT-токена.

    Параметры:
        token (str): JWT-токен, передаваемый в заголовке запроса.

    Возвращаемое значение:
        dict: Данные пользователя, полученные из токена.

    Исключения:
        - HTTPException (401): Если токен некорректен или истёк.
    """

    try:
        user_data = decode_jwt(token)
        return user_data
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )
