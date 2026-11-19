# app/application/logging/use_cases/publish_event.py

from dataclasses import dataclass
from typing import Any

from app.application.ports.event_publisher import EventPublisherPort


@dataclass
class PublishEventUseCase:
    publisher: EventPublisherPort

    async def execute(self, event: Any) -> None:
        await self.publisher.publish(event)