from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import database_helper
from app.security import get_current_user
from app.tasks import (
    TaskBase,
    TaskResponse,
    TaskUpdate,
    complete_task,
    create_task,
    delete_all_tasks,
    delete_task,
    get_tasks,
    update_task,
)

"""
Модуль для работы с задачами API.

Этот модуль содержит маршруты для выполнения CRUD операций с задачами:
создание, получение, обновление, завершение и удаление задач, а также удаление всех задач пользователя.
Используется FastAPI для обработки запросов и взаимодействия с базой данных через SQLAlchemy.
"""
router = APIRouter(prefix="/api/v1/tasks")


@router.post("/me/", response_model=TaskResponse)
async def create_task_route(
    task: TaskBase,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Создание новой задачи для текущего пользователя.

    Принимает данные задачи, создает задачу в базе данных и возвращает её.

    Параметры:
    - task (TaskBase): Данные задачи (заголовок, описание, дедлайн).
    - db (AsyncSession): Сессия базы данных.
    - current_user (dict): Данные текущего пользователя, извлекаются из JWT токена.

    Возвращает:
    - TaskResponse: Созданная задача.
    """
    user_id = int(current_user["sub"])

    new_task = await create_task(
        db=db,
        title=task.title,
        description=task.description,
        user_id=user_id,
        deadline=task.deadline,
    )
    return new_task


@router.get("/me/", response_model=list[TaskResponse])
async def get_tasks_route(
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Получение списка всех задач текущего пользователя.

    Возвращает все задачи, которые принадлежат текущему пользователю.

    Параметры:
    - db (AsyncSession): Сессия базы данных.
    - current_user (dict): Данные текущего пользователя, извлекаются из JWT токена.

    Возвращает:
    - list[TaskResponse]: Список задач пользователя.
    """
    user_id = int(current_user["sub"])

    tasks = await get_tasks(db=db, user_id=user_id)
    return tasks


@router.put("/me/{task_id}/complete/", response_model=dict)
async def complete_task_route(
    task_id: int,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Завершение задачи.

    Обновляет статус задачи на "завершена" для указанного пользователя.

    Параметры:
    - task_id (int): Идентификатор задачи.
    - db (AsyncSession): Сессия базы данных.
    - current_user (dict): Данные текущего пользователя, извлекаются из JWT токена.

    Возвращает:
    - TaskResponse: Обновленная задача.

    Исключения:
    - HTTPException: Если задача не найдена, генерируется ошибка 404.
    """
    user_id = int(current_user["sub"])

    await complete_task(db=db, task_id=task_id, user_id=user_id)

    return {"message" : "Задача выполнена =)"}


@router.patch("/me/update/", response_model=TaskResponse)
async def update_task_route(
    task: TaskUpdate,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Обновление данных существующей задачи.

    Обновляет данные задачи для текущего пользователя, включая заголовок, описание и дедлайн.

    Параметры:
    - task (TaskUpdate): Обновленные данные задачи.
    - db (AsyncSession): Сессия базы данных.
    - current_user (dict): Данные текущего пользователя, извлекаются из JWT токена.

    Возвращает:
    - TaskResponse: Обновленная задача.
    """
    new_task = await update_task(
        db=db,
        task_id=task.id,
        user_id=int(current_user["sub"]),
        title=task.title,
        deadline=task.deadline,
        description=task.description,
    )
    return new_task


@router.delete("/me/{task_id}/")
async def delete_task_route(
    task_id: int,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Удаление задачи.

    Удаляет задачу с указанным идентификатором, если она принадлежит текущему пользователю.

    Параметры:
    - task_id (int): Идентификатор задачи.
    - db (AsyncSession): Сессия базы данных.
    - current_user (dict): Данные текущего пользователя, извлекаются из JWT токена.

    Возвращает:
    - TaskResponse: Удаленная задача.

    Исключения:
    - HTTPException: Если задача не найдена, генерируется ошибка 404.
    """
    user_id = int(current_user["sub"])

    await delete_task(db=db, task_id=task_id, user_id=user_id)

    return {"message": "Задача успешно удалена."}


@router.delete("/me/", response_model=dict)
async def delete_all_tasks_route(
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Удаление всех задач текущего пользователя.

    Удаляет все задачи, принадлежащие текущему пользователю.

    Параметры:
    - db (AsyncSession): Сессия базы данных.
    - current_user (dict): Данные текущего пользователя, извлекаются из JWT токена.

    Возвращает:
    - dict: Сообщение об успешном удалении всех задач.

    Исключения:
    - HTTPException: Если возникла ошибка при удалении задач, генерируется ошибка 404.
    """
    user_id = int(current_user["sub"])

    try:
        await delete_all_tasks(db=db, user_id=user_id)
        return {"message": "Все задачи удалены."}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найдено задач для удаления",
        )
