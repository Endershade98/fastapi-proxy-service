# app/application/proxy/use_cases/cache_management.py
from typing import Optional, Callable
from app.domain.services.cache_service_interface import CacheServiceInterface
from app.domain.value_objects.cache_entry import CacheEntry

class CacheManager:
    def __init__(self, cache_service: CacheServiceInterface):
        self.cache_service = cache_service

    async def get_or_set(self, key: str, value_supplier: Callable[[], dict], ttl: int = 60) -> CacheEntry:
        cached_entry: Optional[CacheEntry] = await self.cache_service.get(key)
        if cached_entry and not cached_entry.is_expired:
            return cached_entry

        value = await value_supplier()
        entry = CacheEntry(key=key, value=value, ttl=ttl)
        await self.cache_service.set(entry)
        return entry