from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    class Config:
        # Включаем использование атрибутов для сериализации
        from_attributes = True
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        # Включаем использование атрибутов для сериализации
        from_attributes = True
        orm_mode = True

