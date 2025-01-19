"""
Этот файл содержит асинхронные функции для получения задач по ID и проверки принадлежности задачи пользователю.

Основные функции:
    - get_task_by_id: Получение задачи по её ID и ID пользователя.

Исключения:
    - HTTPException (404): Если задача не найдена или не принадлежит пользователю.
"""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Task


async def get_task_by_id(*, db: AsyncSession, user_id: int, task_id: int):
    """
    Получает задачу по её ID, проверяя, принадлежит ли она указанному пользователю.

    Параметры:
        db (AsyncSession): Сессия для взаимодействия с базой данных.
        user_id (int): ID пользователя, которому должна принадлежать задача.
        task_id (int): ID задачи, которую нужно получить.

    Возвращаемое значение:
        Task: Задача, если она найдена и принадлежит пользователю.

    Исключения:
        - HTTPException (404): Если задача не найдена или не принадлежит пользователю.
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
