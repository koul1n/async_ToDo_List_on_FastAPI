from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task
from sqlalchemy.future import select

async def create_task(db : AsyncSession, title: str, description: str = None):
    task = Task(title = title, description = description)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

# Получение всех задач
async def get_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()


async def complete_task(db: AsyncSession, task_id: int):
    task = await db.get(Task, task_id)
    if task:
        task.is_completed = True
        await db.commit()
        await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task_id: int):
    task = await db.get(Task, task_id)
    if task:
        await db.delete(task)
        await db.commit()
    return task

async def delete_all_tasks(db: AsyncSession):
    async with db.begin():
        await db.execute(delete(Task))
