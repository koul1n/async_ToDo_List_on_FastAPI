"""
Этот файл содержит класс Settings, который используется для получения параметров конфигурации приложения
из переменных окружения. Он включает настройки для подключения к основной и тестовой базам данных,
а также параметры для сервера.
"""

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    """
    Класс для загрузки и хранения конфигурационных параметров приложения из переменных окружения.

    Атрибуты:
        DRIVER (str): Драйвер базы данных (например, 'postgresql').
        USERNAME (str): Имя пользователя для подключения к основной базе данных.
        PASS (str): Пароль для подключения к основной базе данных.
        HOST (str): Хост для подключения к основной базе данных.
        PORT (int): Порт для подключения к основной базе данных.
        NAME (str): Имя основной базы данных.
        USERNAME_TEST (str): Имя пользователя для подключения к тестовой базе данных.
        PASS_TEST (str): Пароль для подключения к тестовой базе данных.
        HOST_TEST (str): Хост для подключения к тестовой базе данных.
        PORT_TEST (int): Порт для подключения к тестовой базе данных.
        NAME_TEST (str): Имя тестовой базы данных.
        SERVER_HOST (str): Хост сервера приложения.
        SERVER_PORT (int): Порт сервера приложения.

    Методы:
        dsn(): Формирует строку подключения для основной базы данных.
        dsn_for_test(): Формирует строку подключения для тестовой базы данных.
    """

    DRIVER: str = os.getenv("DB_DRIVER")

    USERNAME: str = os.getenv("DB_USERNAME")
    PASS: str = os.getenv("DB_PASS")
    HOST: str = os.getenv("DB_HOST")
    PORT: int = os.getenv("DB_PORT")
    NAME: str = os.getenv("DB_NAME")

    USERNAME_TEST: str = os.getenv("DB_TEST_USERNAME")
    PASS_TEST: str = os.getenv("DB_TEST_PASS")
    HOST_TEST: str = os.getenv("DB_TEST_HOST")
    PORT_TEST: int = os.getenv("DB_TEST_PORT")
    NAME_TEST: str = os.getenv("DB_TEST_NAME")

    SERVER_HOST: str = os.getenv("SERVER_HOST")

    SERVER_PORT: int = os.getenv("SERVER_PORT")

    EXIT_CODE_ERROR: int = 1

    def dsn(self):
        return f"{self.DRIVER}://{self.USERNAME}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"

    def dsn_for_test(self):
        return f"{self.DRIVER}://{self.USERNAME_TEST}:{self.PASS_TEST}@{self.HOST_TEST}:{self.PORT_TEST}/{self.NAME_TEST}"


settings = Settings()
