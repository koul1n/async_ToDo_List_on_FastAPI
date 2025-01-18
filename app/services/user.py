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
    Получение пользователя из базы данных.

    Эта функция позволяет получить пользователя по одному из переданных параметров:
    email, user_id или username. Если ни один параметр не указан, возвращается None.

    Параметры:
    - db (AsyncSession): Асинхронная сессия базы данных.
    - email (EmailStr, optional): Email пользователя. Если указан, поиск производится по email.
    - user_id (int, optional): Идентификатор пользователя. Если указан, поиск производится по user_id.
    - username (str, optional): Имя пользователя. Если указано, поиск производится по username.

    Возвращает:
    - User: Найденный пользователь или None, если пользователь не найден или параметры не указаны.

    Примечание:
    - Если указано несколько параметров (email, user_id, username), используется только первый из них.
    - При отсутствии всех параметров возвращается None.
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

async def change_username(*, db : AsyncSession, user : User, new_username : str):
    existing_user = await get_user(db=db, username=new_username)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с именем {new_username} уже существует.",
        )
    user.username = new_username

async def change_email(*, db : AsyncSession, user : User, new_email : EmailStr):
    existing_user = await get_user(db=db, email=new_email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с email {new_email} уже существует.",
        )
    user.email = new_email