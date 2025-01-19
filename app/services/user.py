"""

Этот файл содержит асинхронные функции для получения пользователей по различным параметрам, а также для изменения их данных (например, имени и email).

Основные функции:
    - get_user: Получение пользователя по email, ID или имени пользователя.
    - change_username: Изменение имени пользователя.
    - change_email: Изменение email пользователя.

Исключения:
    - HTTPException (404): Если пользователь не найден.
    - HTTPException (400): Если имя или email уже заняты другим пользователем.
"""

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User


async def get_user(
    *,
    db: AsyncSession,
    email: EmailStr = None,
    user_id: int = None,
    username: str = None,
):
    """
    Получает пользователя по указанным данным (email, ID или имени).

    Параметры:
        db (AsyncSession): Сессия для взаимодействия с базой данных.
        email (EmailStr, optional): Email пользователя для поиска.
        user_id (int, optional): ID пользователя для поиска.
        username (str, optional): Имя пользователя для поиска.

    Возвращаемое значение:
        User: Пользователь, если найден.

    Исключения:
        - HTTPException (404): Если пользователь не найден.
    """

    if email:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()
    elif user_id:
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()
    elif username:
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден."
    )


async def change_username(*, db: AsyncSession, user: User, new_username: str):
    """
    Изменяет имя пользователя, если оно не занято другим пользователем.

    Параметры:
        db (AsyncSession): Сессия для взаимодействия с базой данных.
        user (User): Пользователь, чьё имя нужно изменить.
        new_username (str): Новое имя пользователя.

    Исключения:
        - HTTPException (400): Если имя уже занято другим пользователем.
    """
    existing_user = await get_user(db=db, username=new_username)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с именем {new_username} уже существует.",
        )
    user.username = new_username


async def change_email(*, db: AsyncSession, user: User, new_email: EmailStr):
    """
    Изменяет email пользователя, если он не занят другим пользователем.

    Параметры:
        db (AsyncSession): Сессия для взаимодействия с базой данных.
        user (User): Пользователь, чей email нужно изменить.
        new_email (EmailStr): Новый email пользователя.

    Исключения:
        - HTTPException (400): Если email уже занят другим пользователем.
    """
    existing_user = await get_user(db=db, email=new_email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с email {new_email} уже существует.",
        )
    user.email = new_email
