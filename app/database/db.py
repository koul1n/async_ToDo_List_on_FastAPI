from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@127.0.0.1/postgres"

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем фабрику сессий
async_session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit = False
)

# Асинхронная функция для получения сессии
async def get_db():
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
