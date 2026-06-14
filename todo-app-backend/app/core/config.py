import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str  
    cors_allowed_origin: list[str]
    
    
def get_settings() -> Settings:
    return Settings(
        os.getenv("DATABASE_URL"),
        os.getenv("CORS_ORIGINS").split(",")
    )
