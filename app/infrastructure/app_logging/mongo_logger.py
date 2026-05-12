# app/infrastructure/logging/mongo_logger.py

from app.domain.ports.logger_port import LoggerPort
from app.infrastructure.celery.tasks.log_tasks import log_event_task


class MongoLogger(LoggerPort):

    def __init__(self, collection=None):
        # collection NON serve più direttamente
        self.collection = collection

    async def log(self, event):
        # Invece di scrivere direttamente su MongoDB, delega a un task Celery
        log_event_task.delay(event.event_type, event.message)