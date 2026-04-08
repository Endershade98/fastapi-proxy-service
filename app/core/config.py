import os 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_PORT: int = os.getenv("REDIS_PORT", 6379)
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")

settings = Settings()