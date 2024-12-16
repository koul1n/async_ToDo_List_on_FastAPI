from pydantic import BaseModel
from datetime import datetime



class TaskBase(BaseModel):
    title: str
    description: str | None = None
    deadline: datetime | None = None

    class Config:
        # Включаем использование атрибутов для сериализации
        from_attributes = True
        orm_mode = True


# Схема для возвращаемой задачи (с id и is_completed)
class TaskResponse(TaskBase):
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    deadline: datetime | None = None

    class Config:
        # Включаем использование атрибутов для сериализации
        from_attributes = True
        orm_mode = True
