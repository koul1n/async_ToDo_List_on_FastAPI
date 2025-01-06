from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    SECRET_KEY: str = "SECRET_KEY"
    ALGORITHM: str = "HS256"
    expires_in: int = 15

auth_settings = AuthSettings()