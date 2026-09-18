# app/domain/ports/event_publisher_port.py

from abc import ABC, abstractmethod
from typing import Any


class EventPublisherPort(ABC):

    @abstractmethod
    async def publish(self, event: Any) -> None:
        raise NotImplementedError