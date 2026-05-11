# app/infrastructure/db/postgres.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_DATABASE_USER}:{settings.POSTGRES_DATABASE_PASSWORD}@{settings.POSTGRES_DATABASE_HOST}:{settings.POSTGRES_DATABASE_PORT}/{settings.POSTGRES_DATABASE_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Dependency for FastAPI
async def get_db():
    async with async_session() as session:
        yield session