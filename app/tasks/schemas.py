from datetime import datetime

from pydantic import BaseModel, ConfigDict, constr

"""
Модуль для определения моделей данных для задачи в API.

Этот модуль включает Pydantic модели, которые описывают структуры данных для создания, обновления и ответа на запросы о задачах.
Модели используются для валидации данных и представления их в нужном формате при взаимодействии с API.
"""


class TaskBase(BaseModel):
    """
    Базовая модель для задачи.

    Эта модель используется для создания задач и описания их базовых характеристик,
    таких как заголовок, описание и дедлайн.

    Атрибуты:
    - title (str): Заголовок задачи (обязательный параметр, минимальная длина 3 символа).
    - description (str | None): Описание задачи (необязательный параметр).
    - deadline (datetime | None): Дата и время дедлайна задачи (необязательный параметр).
    """

    title: constr(min_length=3)
    description: str | None = None
    deadline: datetime | None = None

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
    - is_completed (bool): Статус выполнения задачи.
    - created_at (datetime): Время создания задачи.
    """

    id: int
    is_completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    """
    Модель для обновления данных о задаче.

    Эта модель используется для обновления существующей задачи. Можно обновить только определённые поля,
    такие как заголовок, описание и дедлайн.

    Атрибуты:
    - id (int): Идентификатор задачи, которую необходимо обновить.
    - title (str | None): Новый заголовок задачи (необязательный параметр).
    - description (str | None): Новое описание задачи (необязательный параметр).
    - deadline (datetime | None): Новый дедлайн задачи (необязательный параметр).
    """

    id: int
    title: constr(min_length=3) | None
    description: str | None = None
    deadline: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
