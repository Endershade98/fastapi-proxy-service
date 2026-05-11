# app/domain/ports/rate_limiter_port.py

from abc import ABC, abstractmethod


class RateLimiterPort(ABC):

    @abstractmethod
    async def increment(
        self,
        key: str,
        window_seconds: int
    ) -> int:
        """
        Increment current usage counter
        and return updated count.
        """
        raise NotImplementedError