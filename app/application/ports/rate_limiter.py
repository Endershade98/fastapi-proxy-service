# app/application/ports/rate_limiter.py

from abc import ABC, abstractmethod


class RateLimiterPort(ABC):
    """
    Application port for rate-limit state management.

    The application knows that it can increment a counter.
    It does not know whether the implementation uses Redis,
    another datastore, or an in-memory mechanism.
    """

    @abstractmethod
    async def increment(
        self,
        key: str,
        window_seconds: int,
    ) -> int:
        raise NotImplementedError