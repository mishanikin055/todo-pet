from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    completed: bool
    created_at: datetime
    
class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None
    
class TaskCreateSchema(BaseModel):
    title: str
