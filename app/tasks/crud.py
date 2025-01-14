from http.client import HTTPException
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task
from sqlalchemy.future import select
from sqlalchemy import delete
from datetime import datetime


async def create_task(
    db: AsyncSession,
    user_id: int,
    title: str,
    description: str = None,
    deadline: datetime | None = None,
):
    task = Task(
        owner_id=user_id, title=title, description=description, deadline=deadline
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def update_task(
        db : AsyncSession,
        user_id : int,
        task_id : int,
        title : str | None = None,
        description : str | None = None,
        deadline: datetime | None = None
):
    result = await db.execute(select(Task).filter(Task.id == task_id).filter(Task.owner_id == user_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    if title:
        task.title = title

    if description:
        task.description = description

    if deadline:
        task.deadline = deadline

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
