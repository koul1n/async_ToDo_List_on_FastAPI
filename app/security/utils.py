from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import HTTPException, status

from app.security.config import auth_settings

"""
Модуль для обработки операций с паролями и создания/проверки JWT токенов.

Этот модуль предоставляет функции для хэширования паролей, их проверки, а также
создания и декодирования JWT токенов для аутентификации и авторизации пользователей.
"""


def hash_password(pwd: str) -> str:
    """
    Хэширует пароль с использованием алгоритма bcrypt.

    Эта функция принимает пароль в виде строки, хэширует его и возвращает строку,
    представляющую хэшированный пароль.
    """
    hashed_bytes = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")  # Преобразование байтов в строку


def validate_password(pwd: str, hashed_pwd: str) -> bool:
    """
    Проверяет, совпадает ли введённый пароль с хэшированным.

    Эта функция проверяет введённый пароль с уже сохранённым хэшом пароля и возвращает
    `True`, если пароли совпадают, и `False` в противном случае.

    """
    return bcrypt.checkpw(password=pwd.encode(), hashed_password=hashed_pwd.encode())


def create_jwt(
    data: dict,
    key: str = auth_settings.SECRET_KEY,
    algorithm: str = auth_settings.ALGORITHM,
) -> str:
    """
    Создаёт JWT токен для указанного пользователя.

    Эта функция принимает данные пользователя, добавляет время истечения токена и
    генерирует JWT токен, который используется для аутентификации и авторизации.

    """
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
    """
    Декодирует и проверяет JWT токен.

    Эта функция принимает токен и пытается его декодировать. Если токен действителен,
    возвращает данные из токена. В случае ошибок (например, истёкший токен или неверный токен)
    выбрасывает исключение HTTPException с соответствующим кодом ошибки.

    :param token: JWT токен для декодирования.
    :param key: Секретный ключ для проверки подписи токена.
    :param algorithm: Алгоритм для проверки подписи токена.
    :return: Декодированные данные из токена.
    :raises HTTPException: В случае ошибок с токеном (например, истёкший или неверный).
    """
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
