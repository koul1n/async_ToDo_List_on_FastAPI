from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_session
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@127.0.0.1/postgres"



engine = create_async_engine(DATABASE_URL, echo=True)


async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
)



async def get_db():
    async with async_session() as session:
        yield session





