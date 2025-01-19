"""
Модуль для работы с задачами API.
"""

from .crud import (
    update_task_status,
    create_task,
    delete_all_tasks,
    delete_task,
    get_tasks,
    update_task,
)
from .schemas import TaskBase, TaskResponse, TaskUpdate, TaskUpdateStatus
from .tasks_routes import router
