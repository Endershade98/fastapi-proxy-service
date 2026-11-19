# app/infrastructure/celery/event_publisher.py

from app.application.ports.event_publisher import (
    EventPublisherPort,
)
from app.infrastructure.celery.tasks.log_tasks import (
    log_event_task,
)


class CeleryEventPublisher(EventPublisherPort):

    async def publish(self, event) -> None:
        payload = {
            "event_type": event.__class__.__name__,
            "data": self._serialize_event(event),
        }

        log_event_task.delay(payload)

    @staticmethod
    def _serialize_event(event) -> dict:
        data = {}

        for key, value in vars(event).items():
            if hasattr(value, "value"):
                data[key] = value.value
            elif hasattr(value, "isoformat"):
                data[key] = value.isoformat()
            elif hasattr(value, "__dict__"):
                data[key] = str(value)
            else:
                data[key] = value

        return data