from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

"""
Модуль для настройки параметров аутентификации с использованием Pydantic и переменных окружения.

Этот модуль загружает параметры из `.env` файла и предоставляет конфигурацию для аутентификации, 
включая секретный ключ, алгоритм шифрования и срок действия токенов.
"""

load_dotenv()


class AuthSettings(BaseSettings):
    """
      Класс для управления настройками аутентификации.

      Этот класс загружает параметры из переменных окружения, которые используются
      для генерации и проверки JWT токенов.

      Атрибуты:
          SECRET_KEY (str): Секретный ключ для создания и проверки токенов.
          ALGORITHM (str): Алгоритм для подписи токенов (например, 'HS256').
          expires_in (int): Время жизни токена в минутах (по умолчанию 15 минут).
      """

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    expires_in: int = 15

auth_settings = AuthSettings()

"""
Экземпляр класса AuthSettings для получения конфигурации аутентификации.
"""