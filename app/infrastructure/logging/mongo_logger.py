# app/infrastructure/logging/mongo_logger.py
import logging
from app.domain.services.logging_interface import LoggingInterface
from app.domain.events.log_event import LogEvent


class MongoLogger(LoggingInterface):
    def __init__(self, collection):
        self.collection = collection

    async def log(self, event: LogEvent) -> None:
        try:
            await self.collection.insert_one(event.to_dict())
        except Exception as e:
            logging.error(f"[MongoLogger ERROR] {e}")