# backend/app/core/config.py
from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Configuration Manager"
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    
    # Redis settings
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]  # Vue dev server
    
    class Config:
        env_file = ".env"

settings = Settings()
