# app/infrastructure/db/mongodb.py

from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings


class MongoDB:
    """
    Infrastructure DB wrapper.
    No business logic here (DDD compliance).
    """

    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        self.client = client
        self.db = self.client[db_name]

    def get_collection(self, name: str):
        return self.db[name]


# ---- Factory ----

_client: AsyncIOMotorClient | None = None
_db: MongoDB | None = None


def build_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(settings.MONGO_URI)


def get_mongo() -> MongoDB:
    """
    Singleton-style accessor (safe for FastAPI DI usage).
    """
    global _client, _db

    if _db is None:
        _client = build_mongo_client()
        _db = MongoDB(client=_client, db_name=settings.MONGO_DATABASE_NAME)

    return _db


# ✅ FIX CRITICO: elimina import circolare
# invece di "get_logs_collection" esposto qui,
# la collection viene risolta nel layer logging (DDD correct)
def get_logs_collection():
    """
    Thin helper used by infrastructure logging layer.
    Avoid importing Celery or logger here (NO dependency inversion violation).
    """
    return get_mongo().get_collection("request_logs")