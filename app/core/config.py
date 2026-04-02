import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME")
    REDIS_URL: str = os.getenv("REDIS_URL")
    TIMEOUT: int = os.getenv("TIMEOUT")

    class Config:
        env_file = ".env"

settings = Settings()