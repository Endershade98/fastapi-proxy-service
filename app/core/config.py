import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME")
    REDIS_URL: str = os.getenv("REDIS_URL")
    TIMEOUT: int = os.getenv("TIMEOUT")
    MAX_RETRIES: int = os.getenv("MAX_RETRIES")
    BACKOFF_FACTOR: float = os.getenv("BACKOFF_FACTOR")

    class Config:
        env_file = ".env"

settings = Settings()