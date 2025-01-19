"""
Этот файл содержит класс `AuthSettings`, который используется для загрузки конфигурации аутентификации
из переменных окружения, включая секретный ключ, алгоритм для подписи JWT и время действия токена.

Основные компоненты:
    - AuthSettings: Класс для загрузки параметров аутентификации из переменных окружения.

    Атрибуты:
        - SECRET_KEY (str): Секретный ключ для подписи JWT.
        - ALGORITHM (str): Алгоритм для подписи JWT (например, 'HS256').
        - expires_in (int): Время действия токена в минутах (по умолчанию 15 минут).
"""

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class AuthSettings(BaseSettings):
    """
    Класс для загрузки и хранения параметров аутентификации из переменных окружения.

    Атрибуты:
        SECRET_KEY (str): Секретный ключ для подписи JWT.
        ALGORITHM (str): Алгоритм для подписи JWT.
        expires_in (int): Время действия токена в минутах (по умолчанию 15 минут).
    """

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    expires_in: int = 15


auth_settings = AuthSettings()
