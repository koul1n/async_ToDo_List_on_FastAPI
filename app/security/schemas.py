from pydantic import BaseModel

"""

Этот файл содержит модель `TokenInfo`, которая используется для передачи информации о 
токене аутентификации, включая сам токен и тип токена.
"""


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"
