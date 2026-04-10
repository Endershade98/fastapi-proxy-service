# app/infrastructure/db/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


class MongoDB:

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DATABASE_NAME]

    def get_collection(self, name: str):
        return self.db[name]


mongo = MongoDB()