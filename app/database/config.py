from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
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

    SERVER_HOST:str = os.getenv("SERVER_HOST")

    SERVER_PORT: int = os.getenv("SERVER_PORT")



    def dsn(self):
        return f"{self.DRIVER}://{self.USERNAME}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"

    def dsn_for_test(self):
        return f"{self.DRIVER}://{self.USERNAME_TEST}:{self.PASS_TEST}@{self.HOST_TEST}:{self.PORT_TEST}/{self.NAME_TEST}"


settings = Settings()


