# app/bootstrap/dummies.py

from app.domain.ports.rate_limiter_port import RateLimiterPort
from app.domain.ports.event_publisher_port import EventPublisherPort


class DummyRateLimiter(RateLimiterPort):
    async def increment(self, key: str, window_seconds: int) -> int:
        return 0


class DummyEventPublisher(EventPublisherPort):
    async def publish(self, event) -> None:
        pass