from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from app.models import User
from sqlalchemy.future import select
from fastapi import HTTPException, status


async def create_user(db: AsyncSession, username: str, email: EmailStr, password: str):
    # Проверка на существование пользователя с таким email
    result = await db.execute(select(User).filter(User.email == email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с email {email} уже существует.",
        )


    user = User(username=username, email=email, password=password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_info(db: AsyncSession, user_id: int, new_username: str = None, new_email: EmailStr = None):
    # Получаем пользователя по ID
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден."
        )

    # Проверяем, если новое имя пользователя задано и оно уникально
    if new_username:
        existing_user = await db.execute(select(User).filter(User.username == new_username))
        if existing_user.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователь с именем {new_username} уже существует."
            )
        user.username = new_username

    # Проверяем, если новая почта задана и она уникальна
    if new_email:
        existing_user = await db.execute(select(User).filter(User.email == new_email))
        if existing_user.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователь с email {new_email} уже существует."
            )
        user.email = new_email

    # Сохраняем обновленные данные в базе
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

async def get_user_info(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден."
        )
    return user

async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден."
        )

    await db.execute(delete(User).filter(User.id == user_id))
    await db.commit()

    return {"detail": "Пользователь успешно удален"}


