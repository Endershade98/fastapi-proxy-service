# app/domain/ports/logger_port.py

from abc import ABC, abstractmethod

from app.domain.events.log_event import LogEvent


class LoggerPort(ABC):

    @abstractmethod
    async def log(self, event: LogEvent) -> None:
        raise NotImplementedError