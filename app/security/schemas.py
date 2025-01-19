from pydantic import BaseModel


class TokenInfo(BaseModel):
    """
    Модель данных для информации о токене.

    Этот класс представляет собой модель для хранения информации о JWT-токене, включая сам токен
    и его тип. Он используется для передачи данных о токене клиенту.

    Атрибуты:
        access_token (str): Строка, представляющая сам JWT-токен.
        token_type (str): Тип токена (по умолчанию "Bearer").
    """

    access_token: str
    token_type: str = "Bearer"
