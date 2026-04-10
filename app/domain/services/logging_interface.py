# app/domain/services/logging_interface.py
from abc import ABC, abstractmethod
from app.domain.events.log_event import LogEvent


class LoggingInterface(ABC):

    @abstractmethod
    async def log(self, event: LogEvent) -> None:
        pass