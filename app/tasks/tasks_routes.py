"""
Этот файл содержит маршруты для выполнения CRUD операций с задачами:
создание, получение, обновление, завершение и удаление задач, а также удаление всех задач пользователя.
Используется FastAPI для обработки запросов и взаимодействия с базой данных через SQLAlchemy.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import database_helper
from app.security import get_current_user
from app.tasks import (
    TaskBase,
    TaskResponse,
    TaskUpdate,
    update_task_status,
    create_task,
    delete_all_tasks,
    delete_task,
    get_tasks,
    update_task,
    TaskUpdateStatus,
)


router = APIRouter(prefix="/api/v1/tasks")


@router.post("/me/", response_model=TaskResponse)
async def create_task_route(
    task: TaskBase,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Создает новую задачу для текущего пользователя.

    Параметры:
        task (TaskBase): Объект с данными для создания задачи.
        db (AsyncSession): Сессия для взаимодействия с базой данных.
        current_user (dict): Данные текущего пользователя, извлеченные из JWT токена.

    Возвращаемое значение:
        TaskResponse: Ответ с данными о созданной задаче.

    Исключения:
        - HTTPException (401): Если пользователь не авторизован.
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
    Получает все задачи текущего пользователя.

    Параметры:
        db (AsyncSession): Сессия для взаимодействия с базой данных.
        current_user (dict): Данные текущего пользователя, извлеченные из JWT токена.

    Возвращаемое значение:
        list[TaskResponse]: Список задач текущего пользователя.

    Исключения:
        - HTTPException (401): Если пользователь не авторизован.
    """

    user_id = int(current_user["sub"])

    tasks = await get_tasks(db=db, user_id=user_id)
    return tasks


@router.put("/me/{task_id}/status/", response_model=dict)
async def change_status_task_route(
    task: TaskUpdateStatus,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Изменяет статус задачи для текущего пользователя.

    Параметры:
        task (TaskUpdateStatus): Объект с новыми данными для обновления статуса задачи.
        db (AsyncSession): Сессия для взаимодействия с базой данных.
        current_user (dict): Данные текущего пользователя, извлеченные из JWT токена.

    Возвращаемое значение:
        dict: Сообщение об успешном изменении статуса задачи.

    Исключения:
        - HTTPException (401): Если пользователь не авторизован.
        - HTTPException (404): Если задача не найдена или не принадлежит пользователю.
    """

    user_id = int(current_user["sub"])

    await update_task_status(
        db=db, task_id=task.id, user_id=user_id, new_status=task.new_status
    )

    return {"message": f"Статус задачи изменен."}


@router.patch("/me/update/", response_model=TaskResponse)
async def update_task_route(
    task: TaskUpdate,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Обновляет данные задачи для текущего пользователя.

    Параметры:
        task (TaskUpdate): Объект с данными для обновления задачи.
        db (AsyncSession): Сессия для взаимодействия с базой данных.
        current_user (dict): Данные текущего пользователя, извлеченные из JWT токена.

    Возвращаемое значение:
        TaskResponse: Ответ с данными обновленной задачи.

    Исключения:
        - HTTPException (401): Если пользователь не авторизован.
        - HTTPException (404): Если задача не найдена или не принадлежит пользователю.
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
    Удаляет задачу по ID для текущего пользователя.

    Параметры:
        task_id (int): ID задачи, которую нужно удалить.
        db (AsyncSession): Сессия для взаимодействия с базой данных.
        current_user (dict): Данные текущего пользователя, извлеченные из JWT токена.

    Возвращаемое значение:
        dict: Сообщение об успешном удалении задачи.

    Исключения:
        - HTTPException (401): Если пользователь не авторизован.
        - HTTPException (404): Если задача не найдена или не принадлежит пользователю.
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
    Удаляет все задачи текущего пользователя.

    Параметры:
        db (AsyncSession): Сессия для взаимодействия с базой данных.
        current_user (dict): Данные текущего пользователя, извлеченные из JWT токена.

    Возвращаемое значение:
        dict: Сообщение об успешном удалении всех задач.

    Исключения:
        - HTTPException (401): Если пользователь не авторизован.
        - HTTPException (404): Если нет задач для удаления.
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
