# domain/services/rate_limiter_interface.py
from abc import ABC, abstractmethod


class RateLimiterInterface(ABC):

    @abstractmethod
    async def increment(self, key: str, window: int) -> int:
        pass