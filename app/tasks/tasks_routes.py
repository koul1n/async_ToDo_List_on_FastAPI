from fastapi import APIRouter, Depends, HTTPException, status
from app.tasks import (
    TaskResponse,
    TaskBase,
    create_task,
    complete_task,
    delete_task,
    delete_all_tasks,
    get_tasks,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import database_helper
from app.security import get_current_user


router = APIRouter(prefix="/api/v1/tasks")


@router.post("/me/", response_model=TaskResponse)
async def create_task_route(
    task: TaskBase,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
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
    user_id = int(current_user["sub"])

    tasks = await get_tasks(db=db, user_id=user_id)
    return tasks


@router.put("/me/{task_id}/complete/", response_model=TaskResponse)
async def complete_task_route(
    task_id: int,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = int(current_user["sub"])

    task = await complete_task(db=db, task_id=task_id, user_id=user_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    return task


@router.delete("/me/{task_id}/", response_model=TaskResponse)
async def delete_task_route(
    task_id: int,
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = int(current_user["sub"])

    task = await delete_task(db=db, task_id=task_id, user_id=user_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    return task


@router.delete("/me/", response_model=dict)
async def delete_all_tasks_route(
    db: AsyncSession = Depends(database_helper.get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = int(current_user["sub"])

    try:
        await delete_all_tasks(db=db, user_id=user_id)
        return {"message": "Все задачи удалены."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
