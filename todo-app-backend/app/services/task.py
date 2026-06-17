from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.task import TaskRepository
from app.cache.redis import RedisCacheBackend
from app.schemas.task import TaskSchema, TaskUpdateSchema, TaskCreateSchema

class TaskNotFound(Exception):
    """Задача не найдена"""
    ...

class TaskService:
    def __init__(self,
        db: Session, cache_redis_url: str,
        cache_ttl_seconds: int,
        cache_tasks_key: str
    ) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)
        self.cache = RedisCacheBackend(cache_redis_url, cache_ttl_seconds)
        self.cache_tasks_key = cache_tasks_key
    
    def list_tasks(self) -> list[TaskSchema]:
        cached_tasks = self.cache.get(self.cache_tasks_key):
        if cached_tasks:
            return cached_tasks
        
        tasks = self.task_repository.get_all()
        return [TaskSchema.model_validate(task) for task in tasks]
        
    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task_orm = self.task_repository.create_task(task_create.title)
        self.db.commit()
        return TaskSchema.model_validate(task_orm)
        
        
    def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:
        task_for_update = self.task_repository.get_by_id(task_id)
        if task_for_update is None:
            raise TaskNotFound("Задача не найдена")
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed
        if task_update.title is not None:
            task_for_update.title = task_update.title
            
        self.db.commit()
        return TaskSchema.model_validate(task_for_update)
    
    
    def delete_task(self, task_id: str) -> None:
        task_for_delete = self.task_repository.get_by_id(task_id)
        if task_for_delete is None:
            raise TaskNotFound("Задача не найдена")
        self.task_repository.delete(task_for_delete)
        self.db.commit()