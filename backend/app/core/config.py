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
    # Change this from List[str] to str and parse it manually
    CORS_ORIGINS: str = "http://localhost:5174"

    class Config:
        env_file = ".env"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS as a list of strings"""
        if not self.CORS_ORIGINS:
            return []

        # Split by comma and strip whitespace
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
