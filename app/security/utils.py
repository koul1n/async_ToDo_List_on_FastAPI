"""
Этот файл содержит функции для безопасного хэширования паролей, а также для создания и декодирования JWT-токенов.
Функции используются для управления безопасностью в приложении, включая аутентификацию пользователей и защиту паролей.

Основные компоненты:
    - hash_password: Функция для хэширования пароля с использованием bcrypt.
    - validate_password: Функция для проверки пароля с хэшированным значением.
    - create_jwt: Функция для создания JWT-токена.
    - decode_jwt: Функция для декодирования JWT-токена и проверки его действительности.

Исключения:
    - В случае истечения срока действия или некорректного токена возбуждаются исключения HTTPException с кодом 401.
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import HTTPException, status

from app.security.config import auth_settings


def hash_password(pwd: str) -> str:

    hashed_bytes = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")  # Преобразование байтов в строку


def validate_password(pwd: str, hashed_pwd: str) -> bool:

    return bcrypt.checkpw(password=pwd.encode(), hashed_password=hashed_pwd.encode())


def create_jwt(
    data: dict,
    key: str = auth_settings.SECRET_KEY,
    algorithm: str = auth_settings.ALGORITHM,
) -> str:

    expiration_time = datetime.now(timezone.utc) + timedelta(
        minutes=auth_settings.expires_in
    )
    payload = {**data, "exp": expiration_time}
    return jwt.encode(payload, key, algorithm=algorithm)


def decode_jwt(
    token: str,
    key: str = auth_settings.SECRET_KEY,
    algorithm: str = auth_settings.ALGORITHM,
) -> dict:

    try:
        decoded_token = jwt.decode(token, key, algorithms=[algorithm])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
