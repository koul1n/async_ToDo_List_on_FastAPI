"""
Модуль `tasks`.

Этот пакет предназначен для управления задачами пользователя.
Он включает в себя реализацию CRUD-операций, схем данных и маршрутов для работы с задачами.

Содержит:
- `crud.py`: Реализация CRUD-операций для задач.
- `schemas.py`: Схемы данных для работы с задачами (Pydantic модели).
- `tasks_routes.py`: Маршруты API для задач.
"""

from .crud import (
    complete_task,
    create_task,
    delete_all_tasks,
    delete_task,
    get_tasks,
    update_task,
)
from .schemas import TaskBase, TaskResponse, TaskUpdate
from .tasks_routes import router
