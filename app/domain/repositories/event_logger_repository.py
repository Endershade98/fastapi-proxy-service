# app/domain/repositories/event_logger_repository.py

from abc import ABC, abstractmethod
from app.domain.events.log_event import LogEvent


class LoggingInterface(ABC):

    @abstractmethod
    async def log(self, event: LogEvent) -> None:
        pass