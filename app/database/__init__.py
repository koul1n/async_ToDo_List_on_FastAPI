'''Модуль для настройки асинхронного подключения к базе данных с использованием SQLAlchemy
и для управления конфигурацией приложения с использованием Pydantic и переменных окружения.'''
from .config import settings
from .db import database_for_test, database_helper
