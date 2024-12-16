from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task, User
from sqlalchemy.future import select
from fastapi import HTTPException
from http import HTTPStatus
from pydantic import EmailStr


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


async def create_task(
    db: AsyncSession, user_id: int, title: str, description: str = None
):
    task = Task(owner_id=user_id, title=title, description=description)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_tasks(db: AsyncSession, user_id: int):
    result = await db.execute(select(Task).where(Task.owner_id == user_id))
    return result.scalars().all()


async def complete_task(db: AsyncSession, user_id: int, task_id: int):
    task = await db.get(Task, task_id)
    if task and task.owner_id == user_id:
        task.is_completed = True
        await db.commit()
        await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, user_id: int, task_id: int):
    task = await db.get(Task, task_id)
    if task and task.owner_id == user_id:
        await db.delete(task)
        await db.commit()
    return task


# Удаление всех задач пользователя
async def delete_all_tasks(db: AsyncSession, user_id: int):
    await db.execute(delete(Task).where(Task.owner_id == user_id))
    await db.commit()
