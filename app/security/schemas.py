from pydantic import BaseModel

"""
Модуль для определения модели данных, представляющей информацию о токене.

Этот модуль содержит модель `TokenInfo`, которая используется для передачи информации о 
токене аутентификации, включая сам токен и тип токена.
"""

class TokenInfo(BaseModel):
    access_token: str
    token_type : str = "Bearer"