from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    USERNAME: str = os.getenv("DB_USERNAME")
    PASS: str = os.getenv("DB_PASS")
    HOST: str = os.getenv("DB_HOST")
    PORT: int = os.getenv("DB_PORT")
    NAME: str = os.getenv("DB_NAME")

    def dsn(self):
        return f"postgresql+asyncpg://{self.USERNAME}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"

settings = Settings()


