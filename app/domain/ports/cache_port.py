# app/domain/ports/cache_port.py

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.value_objects.cache_entry import CacheEntry


class CachePort(ABC):

    @abstractmethod
    async def get(self, key: str) -> Optional[CacheEntry]:
        raise NotImplementedError

    @abstractmethod
    async def set(self, entry: CacheEntry) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        raise NotImplementedError