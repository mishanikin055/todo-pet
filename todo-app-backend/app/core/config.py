import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str  
    cors_allowed_origin: list[str]
    redis_url: str
    cache_ttl: int
    cache_tasks_key: str
    
def get_settings() -> Settings:
    return Settings(
        os.getenv("DATABASE_URL"),
        os.getenv("CORS_ORIGINS").split(","),
        os.getenv("REDIS_URL"),
        os.getenv("CACHE_TTL"),
        cache_tasks_key="cache:tasks"
    )
