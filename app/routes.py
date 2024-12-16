from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import (
    create_task,
    get_tasks,
    complete_task,
    delete_task,
    delete_all_tasks,
    create_user,
)
from app.schemas import TaskBase, TaskResponse, UserCreate, UserResponse
from http import HTTPStatus


router = APIRouter()


# создание пользователя
@router.post("/users/", response_model=UserResponse)
async def create_user_route(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await create_user(db, user.username, user.email, user.password)
    return new_user


# Создание задачи для пользователя
@router.post("/tasks/{user_id}/", response_model=TaskResponse)
async def create_task_route(
    user_id: int, task: TaskBase, db: AsyncSession = Depends(get_db)
):
    new_task = await create_task(
        db=db, title=task.title, description=task.description, user_id=user_id
    )
    return new_task


# Получение всех задач для пользователя
@router.get("/tasks/{user_id}/", response_model=list[TaskResponse])
async def get_tasks_route(user_id: int, db: AsyncSession = Depends(get_db)):
    tasks = await get_tasks(db, user_id)
    return tasks


# Маршрут для завершения задачи пользователя
@router.put("/tasks/{user_id}/{task_id}/complete", response_model=TaskResponse)
async def complete_task_route(
    user_id: int, task_id: int, db: AsyncSession = Depends(get_db)
):
    task = await complete_task(db, task_id, user_id)
    if task is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")
    return task


# Маршрут для удаления задачи пользователя
@router.delete("/tasks/{user_id}/{task_id}", response_model=TaskResponse)
async def delete_task_route(
    user_id: int, task_id: int, db: AsyncSession = Depends(get_db)
):
    task = await delete_task(db, task_id, user_id)
    if task is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")
    return task


# Удаление всех задач для пользователя
@router.delete("/tasks/{user_id}/", response_model=dict)
async def delete_all_tasks_route(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await delete_all_tasks(db, user_id)
        return {"message": "All tasks deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
