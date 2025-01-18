from http.client import HTTPException
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Task

"""
Модуль для управления задачами пользователя в базе данных с использованием SQLAlchemy и FastAPI.

Этот модуль включает функции для создания, обновления, получения, завершения и удаления задач. 
Каждая операция выполняется асинхронно с использованием SQLAlchemy для взаимодействия с базой данных.
"""


async def get_task_by_id(*, db: AsyncSession, user_id: int, task_id: int):
    """
    Получает задачу пользователя по её ID.

    Эта функция ищет задачу в базе данных по её ID и проверяет, принадлежит ли она указанному пользователю.

    :param db: Объект сессии базы данных (AsyncSession).
    :param user_id: Идентификатор пользователя, которому принадлежит задача.
    :param task_id: Идентификатор задачи.
    :return: Найденная задача.
    """
    result = await db.execute(
        select(Task).filter(Task.id == task_id, Task.owner_id == user_id)
    )
    task = result.scalars().first()
    if task:
        return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача не найдена или не принадлежит пользователю.",
    )
