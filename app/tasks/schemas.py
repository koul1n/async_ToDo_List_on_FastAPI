from pydantic import BaseModel, constr, ConfigDict
from datetime import datetime

class TaskBase(BaseModel):
    title: constr(min_length=3)
    description: str | None = None
    deadline: datetime | None = None

    model_config = ConfigDict(from_attributes=True)




class TaskResponse(TaskBase):
    id: int
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    deadline: datetime | None = None

    model_config = ConfigDict(from_attributes=True)



