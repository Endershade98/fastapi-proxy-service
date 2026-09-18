# app/infrastructure/celery/event_publisher.py

from app.domain.ports.event_publisher_port import EventPublisherPort
from app.infrastructure.celery.tasks.log_tasks import log_event_task


class CeleryEventPublisher(EventPublisherPort):

    async def publish(self, event) -> None:

        payload = {
            "event_type": getattr(event, "event_type", event.__class__.__name__),
            "data": event.__dict__,
        }

        log_event_task.delay(payload)