from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    deadline: datetime | None = None


    class Config:
        from_attributes = True



class TaskResponse(TaskBase):
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    deadline: datetime | None = None


    class Config:
        from_attributes = True



