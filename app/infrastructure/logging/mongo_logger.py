# app/infrastructure/logging/mongo_logger.py
import logging
from app.domain.services.logging_interface import LoggingInterface
from app.domain.events.log_event import LogEvent
from app.infrastructure.db.mongodb import mongo


class MongoLogger(LoggingInterface):
    """
    Infrastructure Adapter:
    prende un Domain Event e lo persiste su MongoDB
    """

    def __init__(self):
        self.collection = mongo.get_collection("logs")

    async def log(self, event: LogEvent) -> None:
        try:
            document = event.to_dict()
            await self.collection.insert_one(document)

        except Exception as e:
            # fallback: non bloccare il sistema per logging failure
            logging.error(f"[MongoLogger ERROR] {e}")