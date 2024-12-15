from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import create_task, get_tasks, complete_task, delete_task
from app.schemas import TaskBase, TaskResponse
from http import HTTPStatus

router = APIRouter()

@router.post("/tasks/", response_model=TaskResponse)
async def create_task_route(task: TaskBase, db: AsyncSession = Depends(get_db)):
    new_task = await create_task(db, task.title, task.description)
    return new_task


@router.get("/tasks/", response_model=list[TaskResponse])
async def get_tasks_route(db: AsyncSession = Depends(get_db)):
    tasks = await get_tasks(db)
    return tasks

# Маршрут для завершения задачи
@router.put("/tasks/{task_id}/complete", response_model=TaskResponse)
async def complete_task_route(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await complete_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")
    return task

# Маршрут для удаления задачи
@router.delete("/tasks/{task_id}", response_model=TaskResponse)
async def delete_task_route(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await delete_task(db, task_id)
    if task is None:
        raise HTTPException(status_code= HTTPStatus.NOT_FOUND, detail="Task not found")
    return task