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
