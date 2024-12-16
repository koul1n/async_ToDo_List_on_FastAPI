from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from app.models import User
from sqlalchemy.future import select
from fastapi import HTTPException
from http import HTTPStatus


async def create_user(db: AsyncSession, username: str, email: EmailStr, password: str):
    # Проверка на существование пользователя с таким email
    result = await db.execute(select(User).filter(User.email == email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Пользователь с email {email} уже существует.",
        )

    user = User(username=username, email=email, password=password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user