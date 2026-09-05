from pydantic import BaseModel, ConfigDict
from datetime import datetime



class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str
    
class CategoryUpdateSchema(BaseModel):
    name: str
    
