# app/application/logging/use_cases/publish_event.py

from dataclasses import dataclass
from app.domain.ports.event_publisher_port import EventPublisherPort


@dataclass
class PublishEventUseCase:

    publisher: EventPublisherPort

    async def execute(self, event) -> None:
        await self.publisher.publish(event)