# app/domain/services/cache_service_interface.py
from abc import ABC, abstractmethod
from app.domain.value_objects.cache_entry import CacheEntry
from typing import Optional

class CacheServiceInterface(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[CacheEntry]:
        pass

    @abstractmethod
    async def set(self, entry: CacheEntry) -> None:
        pass