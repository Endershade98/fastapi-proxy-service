# app/infrastructure/app_logging/mongo_event_publisher.py

from app.domain.ports.event_publisher_port import EventPublisherPort
from app.domain.events.system_events import (
    RequestLoggedEvent,
    RateLimitExceededEvent
)
from app.infrastructure.db.mongodb import get_logs_collection


class MongoEventPublisher(EventPublisherPort):

    async def publish(self, event) -> None:
        collection = get_logs_collection()

        if isinstance(event, RequestLoggedEvent):
            await collection.insert_one({
                "type": "request_logged",
                "event_type": event.event_type,
                "path": event.path,
                "client_ip": event.client_ip,
                "metadata": event.metadata,
                "occurred_at": event.occurred_at.isoformat(),
            })

        elif isinstance(event, RateLimitExceededEvent):
            await collection.insert_one({
                "type": "rate_limit_exceeded",
                "client_ip": event.client_ip,
                "limit": event.limit,
                "window_seconds": event.window_seconds,
                "occurred_at": event.occurred_at.isoformat(),
            })