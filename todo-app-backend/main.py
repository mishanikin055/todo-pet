from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4


app = FastAPI()


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