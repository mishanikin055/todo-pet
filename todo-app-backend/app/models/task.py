from sqlalchemy import func

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class TaskORM(Base):
    __tablename__ = "tasks"
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())