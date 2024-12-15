from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str | None = None

    class Config:
        arbitrary_types_allowed = True

# Схема для возвращаемой задачи (с id и is_completed)
class TaskResponse(TaskBase):
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime


    class Config:
        orm_mode = True  # Это важно для работы с SQLAlchemy моделями
        arbitrary_types_allowed = True
