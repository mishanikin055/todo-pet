import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str  
    cors_allowed_origin: list[str]
    
    
def get_settings() -> Settings:
    return Settings(
        os.getenv("DATAASE_URL"),
        cors_raw = os.getenv("CORS_ORIGINS")
        cors_list = cors_raw.split(",")

        return Settings(DATABASE_URL=db_url, cors_allowed_origin=cors_list)
    )
