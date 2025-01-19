"""
Этот файл содержит схемы данных для операций с пользователями в приложении:
создание, обновление и получение информации о пользователях.
Используется Pydantic для валидации и сериализации данных.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, constr


class UserCreate(BaseModel):
    """
    Схема для создания нового пользователя.

    Атрибуты:
        username (str): Имя пользователя (должно быть от 3 до 20 символов).
        email (EmailStr): Электронная почта пользователя.
        password (str): Пароль пользователя (должен быть от 5 до 20 символов).
    """

    username: constr(min_length=3, max_length=20)
    email: EmailStr
    password: constr(min_length=5, max_length=20)

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    """
    Схема для отображения информации о пользователе.

    Атрибуты:
        username (str): Имя пользователя.
        email (str): Электронная почта пользователя.
        is_active (bool): Статус активности пользователя.
    """

    username: str
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """
    Схема для обновления информации о пользователе.

    Атрибуты:
        username (str | None): Новое имя пользователя (необязательное, если не обновляется).
        email (EmailStr | None): Новый email пользователя (необязательное, если не обновляется).
    """

    username: constr(min_length=3, max_length=20) | None
    email: EmailStr | None
    model_config = ConfigDict(from_attributes=True)
