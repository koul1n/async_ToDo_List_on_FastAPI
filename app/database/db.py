from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .config import settings

"""
Модуль для настройки асинхронного подключения к базе данных с использованием SQLAlchemy.

Этот модуль содержит класс `Database`, который предоставляет методы для создания
асинхронного движка и сессий для работы с базой данных. Также настраиваются
основные подключения для основного приложения и тестов.
"""


class Database:

    def __init__(self, link):
        self.engine = create_async_engine(link, echo=False)
        self.async_session = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False, autocommit=False
        )

    async def get_db(self):
        async with self.async_session() as session:
            yield session


database_helper = Database(settings.dsn())

database_for_test = Database(settings.dsn_for_test())
