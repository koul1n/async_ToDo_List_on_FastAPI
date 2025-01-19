from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, constr


class TaskStatus(str, Enum):
    """
    Перечисление статусов задачи.
    """
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskUpdateStatus(BaseModel):
    id : int
    new_status: TaskStatus



class TaskBase(BaseModel):
    """
    Базовая модель для задачи.

    Эта модель используется для создания задач и описания их базовых характеристик,
    таких как заголовок, описание, дедлайн и статус.

    Атрибуты:
    - title (str): Заголовок задачи (обязательный параметр, минимальная длина 3 символа).
    - description (str | None): Описание задачи (необязательный параметр).
    - deadline (datetime | None): Дата и время дедлайна задачи (необязательный параметр).
    - status (TaskStatus | None): Статус задачи (по умолчанию: NEW).
    """

    title: constr(min_length=3)
    description: str | None = None
    deadline: datetime | None = None
    status: TaskStatus | None = TaskStatus.NEW

    model_config = ConfigDict(from_attributes=True)


class TaskResponse(TaskBase):
    """
    Модель ответа для задачи.

    Эта модель используется для возврата данных о задаче в ответе API, включая ID задачи,
    статус выполнения и время создания.

    Атрибуты:
    - id (int): Идентификатор задачи.
    - title (str): Заголовок задачи.
    - description (str | None): Описание задачи (необязательное поле).
    - deadline (datetime | None): Дата и время дедлайна задачи (необязательное поле).
    - status (TaskStatus): Статус задачи.
    - created_at (datetime): Время создания задачи.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    """
    Модель для обновления данных о задаче.

    Эта модель используется для обновления существующей задачи. Можно обновить только определённые поля,
    такие как заголовок, описание, дедлайн и статус.

    Атрибуты:
    - id (int): Идентификатор задачи, которую необходимо обновить.
    - title (str | None): Новый заголовок задачи (необязательный параметр).
    - description (str | None): Новое описание задачи (необязательный параметр).
    - deadline (datetime | None): Новый дедлайн задачи (необязательный параметр).
    - status (TaskStatus | None): Новый статус задачи (необязательный параметр).
    """

    id: int
    title: constr(min_length=3) | None
    description: str | None = None
    deadline: datetime | None = None
    status: TaskStatus | None = None

    model_config = ConfigDict(from_attributes=True)
