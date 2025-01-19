from datetime import datetime
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.services import get_task_by_id
from app.models import Task


async def create_task(
    db: AsyncSession,
    user_id: int,
    title: str,
    description: str = None,
    deadline: datetime | None = None,
):
    """
    Создаёт новую задачу в базе данных.

    Атрибуты:
        db (AsyncSession): Сессия базы данных.
        user_id (int): Идентификатор пользователя, который создает задачу.
        title (str): Заголовок задачи.
        description (str | None): Описание задачи (необязательное).
        deadline (datetime | None): Дедлайн задачи (необязательное).

    Возвращает:
        task (Task): Созданная задача.
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
    Обновляет существующую задачу в базе данных.

    Атрибуты:
        db (AsyncSession): Сессия базы данных.
        user_id (int): Идентификатор пользователя, который обновляет задачу.
        task_id (int): Идентификатор задачи для обновления.
        title (str | None): Новый заголовок задачи (необязательное).
        description (str | None): Новое описание задачи (необязательное).
        deadline (datetime | None): Новый срок выполнения задачи (необязательное).

    Возвращает:
        task (Task): Обновленная задача.

    Исключения:
        HTTPException: В случае, если задача не найдена.
    """

    task = await get_task_by_id(db=db, task_id=task_id, user_id=user_id)

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

    Атрибуты:
        db (AsyncSession): Сессия базы данных.
        user_id (int): Идентификатор пользователя, чьи задачи нужно получить.

    Возвращает:
        list[Task]: Список задач пользователя.
    """

    result = await db.execute(select(Task).where(Task.owner_id == user_id))
    return result.scalars().all()


async def update_task_status(
    db: AsyncSession, user_id: int, task_id: int, new_status: str
):
    """
    Обновляет статус задачи.

    Атрибуты:
        db (AsyncSession): Сессия базы данных.
        user_id (int): Идентификатор пользователя, который обновляет статус.
        task_id (int): Идентификатор задачи, статус которой нужно обновить.
        new_status (str): Новый статус задачи.

    Возвращает:
        task (Task): Обновленная задача.

    Исключения:
        HTTPException: В случае, если задача не найдена.
    """

    task = await get_task_by_id(db=db, task_id=task_id, user_id=user_id)

    task.status = new_status
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, user_id: int, task_id: int):
    """
    Удаляет задачу из базы данных.

    Атрибуты:
        db (AsyncSession): Сессия базы данных.
        user_id (int): Идентификатор пользователя, который удаляет задачу.
        task_id (int): Идентификатор задачи для удаления.

    Возвращает:
        task (Task): Удаленная задача.

    Исключения:
        HTTPException: В случае, если задача не найдена.
    """

    task = await get_task_by_id(db=db, user_id=user_id, task_id=task_id)
    await db.delete(task)
    await db.commit()
    return task


async def delete_all_tasks(db: AsyncSession, user_id: int):
    """
    Удаляет все задачи пользователя.

    Атрибуты:
        db (AsyncSession): Сессия базы данных.
        user_id (int): Идентификатор пользователя, чьи задачи нужно удалить.

    Возвращает:
        None
    """

    await db.execute(delete(Task).where(Task.owner_id == user_id))
    await db.commit()
