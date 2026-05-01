# app/infrastructure/logging/mongo_logger.py

import logging

from app.domain.events.log_event import LogEvent
from app.domain.repositories.event_logger_repository import LoggingInterface


class MongoLogger(LoggingInterface):
    def __init__(self, collection):
        self.collection = collection

    async def log(self, event: LogEvent) -> None:
        try:
            await self.collection.insert_one(event.to_dict())
        except Exception as e:
            logging.error(f"[MongoLogger ERROR] {e}")