"""
В данном файле содержаться crud функции
для работы с пользователями.
"""
from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import get_user, change_username, change_email
from app.models import User
from app.security import hash_password


async def create_user(db: AsyncSession, username: str, email: EmailStr, password: str):
    """
    Создает нового пользователя.

    Атрибуты:
        db (AsyncSession): Сессия базы данных.
        username (str): Имя пользователя.
        email (EmailStr): Электронная почта пользователя.
        password (str): Пароль пользователя.

    Возвращает:
        user (User): Созданный пользователь.

    Исключения:
        HTTPException: В случае, если пользователь с таким именем или email уже существует.
    """
    existing_user = await get_user(db=db, email=email, username=username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с email {email} или именем {username} уже существует.",
        )

    user = User(username=username, email=email, password=hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_info(
    db: AsyncSession, user_id: int, new_username: str = None, new_email: EmailStr = None
):
    """
    Обновляет информацию о пользователе, включая имя и/или email.

    Атрибуты:
        db (AsyncSession): Сессия базы данных.
        user_id (int): Идентификатор пользователя, чью информацию нужно обновить.
        new_username (str | None): Новое имя пользователя (необязательное).
        new_email (EmailStr | None): Новый email пользователя (необязательное).

    Возвращает:
        user (User): Обновленный пользователь.

    Исключения:
        HTTPException: В случае, если пользователь не найден или обновление данных невозможно.
    """
    user = await get_user(db=db, user_id=user_id)

    if new_username:
        await change_username(db=db, user=user, new_username=new_username)
    if new_email:
        await change_email(db=db, user=user, new_email=new_email)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_user_info(db: AsyncSession, user_id: int):
    """
    Получает информацию о пользователе.

    Атрибуты:
        db (AsyncSession): Сессия базы данных.
        user_id (int): Идентификатор пользователя, информацию о котором нужно получить.

    Возвращает:
        user (User): Информация о пользователе.

    Исключения:
        HTTPException: В случае, если пользователь не найден.
    """

    user = await get_user(db=db, user_id=user_id)

    return user


async def delete_user(db: AsyncSession, user_id: int):
    """
    Удаляет пользователя из базы данных.

    Атрибуты:
        db (AsyncSession): Сессия базы данных.
        user_id (int): Идентификатор пользователя для удаления.

    Возвращает:
        dict: Словарь с подтверждением удаления пользователя.

    Исключения:
        HTTPException: В случае, если пользователь не найден.
    """

    await get_user(db=db, user_id=user_id)

    await db.execute(delete(User).filter(User.id == user_id))
    await db.commit()

    return {"detail": "Пользователь успешно удален"}
