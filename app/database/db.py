from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings


class Database:
    def __init__(self, link):
        self.engine = create_async_engine(link, echo=False)
        self.async_session = async_sessionmaker(bind=self.engine,
                                                autoflush=False,
                                                expire_on_commit=False,
                                                autocommit = False
                                                )


    async def get_db(self):
        async with self.async_session() as session:
            yield session



database_helper = Database(settings.dsn())

database_for_test = Database(settings.dns_for_test())
