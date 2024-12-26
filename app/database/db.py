from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@127.0.0.1/postgres"
from app.database import settings


class Database:
    def __init__(self):
        self.engine = create_async_engine(settings.dsn(), echo=False)
        self.async_session = async_sessionmaker(bind=self.engine,
                                                autoflush=False,
                                                expire_on_commit=False,
                                                autocommit = False
                                                )


    async def get_db(self):
        async with self.async_session() as session:
            yield session


database_helper = Database()


