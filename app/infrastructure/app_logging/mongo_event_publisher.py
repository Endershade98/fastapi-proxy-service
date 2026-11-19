# app/infrastructure/app_logging/mongo_event_publisher.py

from app.application.ports.event_publisher import EventPublisherPort
from app.domain.events.rate_limit import RateLimitExceeded
from app.infrastructure.db.mongodb import get_logs_collection


class MongoEventPublisher(EventPublisherPort):
    async def publish(self, event) -> None:
        collection = get_logs_collection()

        if isinstance(event, RateLimitExceeded):
            await collection.insert_one(
                {
                    "event_type": "RateLimitExceeded",
                    "client_ip": str(event.client_ip),
                    "limit": event.quota.limit,
                    "window_seconds": event.quota.window_seconds,
                    "occurred_at": event.occurred_at,
                }
            )