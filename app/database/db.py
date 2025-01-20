"""
Этот файл содержит реализацию класса для асинхронной работы с базой данных,
включая тестирование подключения и управление сессиями для основной и тестовой базы данных.

Основные компоненты:
    - Класс Database: Обеспечивает создание и управление подключением к базе данных,
      а также создание сессий для работы с данными.
    - Объекты database_helper и database_for_test: Экземпляры класса Database, настроенные для работы с основной
      и тестовой базой данных соответственно.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.exc import SQLAlchemyError
from app.logs import logger
from .config import settings
from sqlalchemy.sql import text
from uuid import uuid4


class Database:
    """
    Класс для работы с базой данных через асинхронный SQLAlchemy.

    Атрибуты:
        engine (AsyncEngine): Асинхронный движок для подключения к базе данных.
        async_session (sessionmaker): Асинхронный фабричный метод для создания сессий.
        log_id (str): Уникальный идентификатор для ведения логов.

    Методы:
        test_connection(): Проверяет подключение к базе данных с выполнением простого запроса.
        get_db(): Генератор для получения сессии подключения к базе данных.
    """

    def __init__(self, link):
        self.engine = create_async_engine(link, echo=False)
        self.async_session = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False, autocommit=False
        )
        self.log_id = str(uuid4())
        logger.bind(log_id=self.log_id).info("Database engine initialized.")

    async def test_connection(self):
        """
        Проверяет подключение к базе данных, выполняя простой запрос.

        Исключения:
            ConnectionError: Подключение не удалось.

        Логирует успех или ошибку при тестировании подключения.
        """
        try:
            async with self.engine.connect() as connection:
                await connection.execute(text("SELECT 1"))  # Обернули запрос в text
                await connection.commit()
            logger.bind(log_id=self.log_id).info("Database connection test successful.")
        except SQLAlchemyError as e:
            logger.bind(log_id=self.log_id).error(
                f"Database connection test failed: {str(e)}"
            )
            raise ConnectionError(f"Database connection failed: {str(e)}")

    async def get_db(self):
        """
        Генератор, создающий и возвращающий асинхронную сессию для работы с базой данных.

        Возвращаемое значение:
            AsyncSession: Асинхронная сессия для взаимодействия с базой данных.

        Логирует успешное подключение к базе данных.
        """
        async with self.async_session() as session:
            logger.bind(log_id=self.log_id).info(
                f"Successfully connected to the database at {self.engine.url}."
            )
            yield session


database_helper = Database(settings.dsn())

database_for_test = Database(settings.dsn_for_test())
