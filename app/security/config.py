from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class AuthSettings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    expires_in: int = 15

auth_settings = AuthSettings()