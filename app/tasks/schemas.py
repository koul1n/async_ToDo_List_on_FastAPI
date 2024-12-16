from pydantic import BaseModel, ConfigDict
from datetime import datetime



class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str | None = None



# Схема для возвращаемой задачи (с id и is_completed)
class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
