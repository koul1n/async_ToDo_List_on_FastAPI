from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str | None = None

    class Config:
        arbitrary_types_allowed = True

# Схема для возвращаемой задачи (с id и is_completed)
class TaskResponse(TaskBase):
    id: int
    is_completed: bool

    class Config:
        orm_mode = True  # Это важно для работы с SQLAlchemy моделями
        arbitrary_types_allowed = True
