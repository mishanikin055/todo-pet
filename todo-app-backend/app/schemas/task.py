from pydantic import BaseModel

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool
    
class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None
    
class TaskCreateSchema(BaseModel):
    title: str
