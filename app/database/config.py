from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = 'postgres'
    DB_PASS: str = 'postgres'
    DB_HOST: str = '127.0.0.1'
    DB_PORT:str = '8000'
    DB_NAME: str = 'postgres'

    def dsn(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}"

settings = Settings()

