from contextlib import asynccontextmanager
import math
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres"

engine = create_engine(DATABASE_URL)

Sessionlocal = sessionmaker[Session](bind=engine)



class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid4)


class TaskORM(Base):
    __tablename__ = "tasks"
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool
    
class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None
    
class TaskCreate(BaseModel):
    title: str

tasks: list[TaskSchema] = []


def get_db():
    db = Sessionlocal()
    
    yield
     
    db.close()

@app.get("/")
def read_base_page():
    return {"message" : "Hello world!"}

@app.get("/tasks")
def read_tasks() -> list[TaskSchema]:
    return tasks


@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)
    return new_task

  
@app.patch("/tasks/{task_id}")
def update_task(
    task_id: str,
    payload: TaskUpdateSchema
):
    edited_task = None
    for task in tasks:
        if task.id == task_id:
            edited_task = task
    if edited_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    if payload.completed is not None:
        edited_task.completed = payload.completed
    if payload.title is not None:
        edited_task.title = payload.title
    
    return edited_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str
):
    tasks[:] = [task for task in tasks if task.id != task_id]