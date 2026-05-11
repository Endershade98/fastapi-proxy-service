# app/config/settings.py

import os 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # REDIS SETTINGS
    REDIS_PORT: int = os.getenv("REDIS_PORT", 6379)
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"

    # CELERY
    USE_CELERY: bool = True
    CELERY_BROKER_URL: str = REDIS_URL
    CELERY_RESULT_BACKEND: str = REDIS_URL
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # in seconds

    # MONGO SETTINGS
    MONGO_DATABASE_NAME: str = os.getenv("MONGO_DATABASE_NAME", "fastapi_proxy_mongo_db")
    MONGO_DATABASE_PORT: int = os.getenv("MONGO_DATABASE_PORT", 27017)
    MONGO_DATABASE_HOST: str = os.getenv("MONGO_DATABASE_HOST", "localhost")
    MONGO_DATABASE_USER: str = os.getenv("MONGO_DATABASE_USER", "proxy_user")
    MONGO_DATABASE_PASSWORD: str = os.getenv("MONGO_DATABASE_PASSWORD", "proxy_password")
    MONGO_URI: str = f"mongodb://{MONGO_DATABASE_USER}:{MONGO_DATABASE_PASSWORD}@{MONGO_DATABASE_HOST}:{MONGO_DATABASE_PORT}/{MONGO_DATABASE_NAME}"
    
    # POSTGRES SETTINGS
    POSTGRES_DATABASE_NAME: str = os.getenv("POSTGRES_DATABASE_NAME", "fastapi_proxy_postgres_db")
    POSTGRES_DATABASE_PORT: int = os.getenv("POSTGRES_DATABASE_PORT", 5432)
    POSTGRES_DATABASE_HOST: str = os.getenv("POSTGRES_DATABASE_HOST", "localhost")
    POSTGRES_DATABASE_USER: str = os.getenv("POSTGRES_DATABASE_USER", "proxy_user")
    POSTGRES_DATABASE_PASSWORD: str = os.getenv("POSTGRES_DATABASE_PASSWORD", "proxy_password")

    # DEBUG
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

    # SECRETS
    KEY_SECRET: str = os.getenv("KEY_SECRET", "default_secret_key")

settings = Settings()