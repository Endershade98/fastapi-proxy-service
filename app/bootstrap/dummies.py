# app/bootstrap/dummies.py

from app.application.ports.event_publisher import (
    EventPublisherPort,
)
from app.application.ports.rate_limiter import (
    RateLimiterPort,
)


class DummyRateLimiter(RateLimiterPort):

    async def increment(
        self,
        key: str,
        window_seconds: int,
    ) -> int:
        return 0


class DummyEventPublisher(EventPublisherPort):

    async def publish(self, event) -> None:
        return None