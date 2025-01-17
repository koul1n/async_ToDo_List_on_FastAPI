from datetime import datetime
from http.client import HTTPException

from fastapi import HTTPException, status
from sqlalchemy import delete
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
    return None

async def create_task(
    db: AsyncSession,
    user_id: int,
    title: str,
    description: str = None,
    deadline: datetime | None = None,
):
    """
    Создает новую задачу для пользователя.

    Эта функция принимает данные для новой задачи, добавляет ее в базу данных,
    коммитит изменения и возвращает созданную задачу.

    :param db: Объект сессии базы данных (AsyncSession).
    :param user_id: Идентификатор пользователя, которому принадлежит задача.
    :param title: Заголовок задачи.
    :param description: Описание задачи (необязательный параметр).
    :param deadline: Дата и время завершения задачи (необязательный параметр).
    :return: Созданная задача.
    """
    task = Task(
        owner_id=user_id, title=title, description=description, deadline=deadline
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def update_task(
    db: AsyncSession,
    user_id: int,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    deadline: datetime | None = None,
):
    """
    Обновляет задачу пользователя по ID.

    Эта функция ищет задачу по ID и обновляет её параметры (заголовок, описание, срок)
    в случае, если задача принадлежит указанному пользователю.

    :param db: Объект сессии базы данных (AsyncSession).
    :param user_id: Идентификатор пользователя, которому принадлежит задача.
    :param task_id: Идентификатор задачи, которую нужно обновить.
    :param title: Новый заголовок задачи (необязательный параметр).
    :param description: Новое описание задачи (необязательный параметр).
    :param deadline: Новый срок выполнения задачи (необязательный параметр).
    :raises HTTPException: В случае, если задача не найдена или не принадлежит пользователю.
    :return: Обновленная задача.
    """

    task = await get_task_by_id(db = db, task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )

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
    """
    Получает все задачи пользователя.

    Эта функция возвращает список всех задач, принадлежащих указанному пользователю.

    :param db: Объект сессии базы данных (AsyncSession).
    :param user_id: Идентификатор пользователя.
    :return: Список задач пользователя.
    """
    result = await db.execute(select(Task).where(Task.owner_id == user_id))
    return result.scalars().all()


async def complete_task(db: AsyncSession, user_id: int, task_id: int):
    """
    Отмечает задачу как выполненную.

    Эта функция изменяет статус задачи на "выполнено", если задача принадлежит указанному пользователю.

    :param db: Объект сессии базы данных (AsyncSession).
    :param user_id: Идентификатор пользователя, которому принадлежит задача.
    :param task_id: Идентификатор задачи, которую необходимо завершить.
    :return: Обновленная задача с пометкой о выполнении.
    """
    task = await get_task_by_id(db = db, task_id=task_id, user_id=user_id)
    if not task:
        raise ValueError("Задача не найдена")
    task.is_completed = True
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, user_id: int, task_id: int):
    """
    Удаляет задачу пользователя по ID.

    Эта функция удаляет задачу из базы данных, если задача принадлежит указанному пользователю.

    :param db: Объект сессии базы данных (AsyncSession).
    :param user_id: Идентификатор пользователя, которому принадлежит задача.
    :param task_id: Идентификатор задачи, которую нужно удалить.
    :return: Удаленная задача.
    """
    task = await get_task_by_id(db = db, user_id=user_id, task_id=task_id)
    if task is None:
        raise ValueError("Задача не найдена.")
    await db.delete(task)
    await db.commit()
    return task


# Удаление всех задач пользователя
async def delete_all_tasks(db: AsyncSession, user_id: int):
    """
    Удаляет все задачи пользователя.

    Эта функция удаляет все задачи, принадлежащие пользователю.

    :param db: Объект сессии базы данных (AsyncSession).
    :param user_id: Идентификатор пользователя, чьи задачи нужно удалить.
    """
    await db.execute(delete(Task).where(Task.owner_id == user_id))
    await db.commit()
