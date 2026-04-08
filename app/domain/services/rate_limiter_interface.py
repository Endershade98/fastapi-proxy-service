# domain/services/rate_limiter_interface.py
from abc import ABC, abstractmethod

class RateLimiterInterface(ABC):
    @abstractmethod
    async def allow(self, request) -> bool:
        pass