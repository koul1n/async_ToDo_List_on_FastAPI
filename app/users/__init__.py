"""
Модуль `users`.

Этот пакет предназначен для управления пользователями приложения.
Он включает в себя реализацию CRUD-операций, схем данных и маршрутов для работы с пользователями.

Содержит:
- `crud.py`: Реализация CRUD-операций для пользователей.
- `schemas.py`: Схемы данных для работы с пользователями (Pydantic модели).
- `users_routes.py`: Маршруты API для пользователей.
"""

from .crud import (
    create_user,
    delete_user,
    get_user,
    get_user_info,
    update_user_info,
)
from .schemas import UserCreate, UserResponse, UserUpdate
from .users_routes import router
