# app/application/ports/cache.py

from abc import ABC, abstractmethod

from app.application.caching.models import CacheEntry


class CachePort(ABC):
    """
    Application port for cache persistence.

    Infrastructure adapters such as Redis implement this contract.
    """

    @abstractmethod
    async def get(self, key: str) -> CacheEntry | None:
        raise NotImplementedError

    @abstractmethod
    async def set(self, entry: CacheEntry) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        raise NotImplementedError