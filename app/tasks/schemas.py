from pydantic import BaseModel, constr, ConfigDict
from datetime import datetime

class TaskBase(BaseModel):
    title: constr(min_length=3)
    description: str | None = None
    deadline: datetime | None = None

    model_config = ConfigDict(from_attributes=True)



class TaskResponse(TaskBase):
    id: int
    is_completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    id : int
    title: constr(min_length=3) | None
    description: str | None = None
    deadline: datetime | None = None

    model_config = ConfigDict(from_attributes=True)




