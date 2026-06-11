from contextlib import asynccontextmanager
import math
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from sqlalchemy import create_engine, select
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
    try:
        yield db
    finally: 
        db.close()

@app.get("/")
def read_base_page():
    return {"message" : "Hello world!"}

def task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)



@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in tasks_from_db]


@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()
    return task_orm_to_model(new_task)

  
@app.patch("/tasks/{task_id}")
def update_task(
    task_id: str,
    payload: TaskUpdateSchema,
    db: Session = Depends(get_db)
) -> TaskSchema:
    task_for_update = db.get(TaskORM, task_id)
    
    if task_for_update is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    if payload.completed is not None:
        task_for_update.completed = payload.completed
    if payload.title is not None:
        task_for_update.title = payload.title
        
    db.commit()
    return task_for_update


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()