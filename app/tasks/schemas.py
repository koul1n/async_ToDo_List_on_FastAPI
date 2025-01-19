"""Этот файл содержит Pydantic модели для задач"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, constr


class TaskStatus(str, Enum):
    """
    Перечисление статусов задачи.

    Статусы:
        NEW: Задача новая.
        IN_PROGRESS: Задача в процессе выполнения.
        COMPLETED: Задача выполнена.
    """

    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskUpdateStatus(BaseModel):
    """
    Модель для обновления статуса задачи.

    Атрибуты:
        id (int): Идентификатор задачи.
        new_status (TaskStatus): Новый статус задачи.
    """

    id: int
    new_status: TaskStatus


class TaskBase(BaseModel):
    """
    Основная модель задачи, которая используется для создания и обновления задачи.

    Атрибуты:
        title (str): Заголовок задачи (должен быть минимум 3 символа).
        description (str | None): Описание задачи (необязательное).
        deadline (datetime | None): Срок выполнения задачи (необязательное).
        status (TaskStatus | None): Статус задачи (по умолчанию "NEW").
    """

    title: constr(min_length=3)
    description: str | None = None
    deadline: datetime | None = None
    status: TaskStatus | None = TaskStatus.NEW

    model_config = ConfigDict(from_attributes=True)


class TaskResponse(TaskBase):
    """
    Модель задачи для ответа API.

    Атрибуты:
        id (int): Идентификатор задачи.
        created_at (datetime): Дата и время создания задачи.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    """
    Модель для обновления данных задачи.

    Атрибуты:
        id (int): Идентификатор задачи.
        title (str | None): Новый заголовок задачи (необязательное).
        description (str | None): Новое описание задачи (необязательное).
        deadline (datetime | None): Новый срок выполнения задачи (необязательное).
        status (TaskStatus | None): Новый статус задачи (необязательное).
    """

    id: int
    title: constr(min_length=3) | None
    description: str | None = None
    deadline: datetime | None = None
    status: TaskStatus | None = None

    model_config = ConfigDict(from_attributes=True)
