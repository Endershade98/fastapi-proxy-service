# app/infrastructure/db/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings


class MongoDB:
    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        self.client = client
        self.db = self.client[db_name]

    def get_collection(self, name: str):
        return self.db[name]


def build_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(settings.MONGO_URI)


def get_mongo() -> MongoDB:
    client = build_mongo_client()
    return MongoDB(client=client, db_name=settings.MONGO_DATABASE_NAME)