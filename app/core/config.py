from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Proxy"
    REDIS_URL: str = "redis://localhost:6379"
    TIMEOUT: int = 5

    class Config:
        env_file = ".env"

settings = Settings()