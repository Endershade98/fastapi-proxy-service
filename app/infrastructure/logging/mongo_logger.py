# app/infrastructure/logging/mongo_logger.py

from app.domain.repositories.event_logger_repository import LoggingInterface
from app.infrastructure.celery.tasks.log_tasks import log_event_task


class MongoLogger(LoggingInterface):

    def __init__(self, collection=None):
        # collection NON serve più direttamente
        self.collection = collection

    async def log(self, event):
        log_event_task.delay(event.to_dict())