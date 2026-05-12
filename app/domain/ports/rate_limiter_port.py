# app/domain/ports/rate_limiter_port.py

from abc import ABC, abstractmethod


class RateLimiterPort(ABC):

    @abstractmethod
    async def is_allowed(self, key: str) -> bool:
        """
        Check if request is allowed under rate limit.
        """
        raise NotImplementedError

    @abstractmethod
    async def increment(self, key: str, window_seconds: int) -> int:
        """
        Increment usage counter and return updated count.
        """
        raise NotImplementedError