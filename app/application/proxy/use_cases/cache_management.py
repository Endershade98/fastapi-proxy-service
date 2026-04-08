# app/application/proxy/use_cases/cache_management.py
from app.core.logging import logger
from typing import Optional, Callable
from app.domain.services.cache_service_interface import CacheServiceInterface
from app.domain.value_objects.cache_entry import CacheEntry

class CacheManager:
    def __init__(self, cache_service: CacheServiceInterface):
        self.cache_service = cache_service

    async def get_or_set(self, key: str, value_supplier: Callable[[], dict], ttl: int = 60) -> CacheEntry:
        cached_entry: Optional[CacheEntry] = await self.cache_service.get(key)
        logger.debug(f"Cache lookup for key '{key}': {'HIT' if cached_entry else 'MISS'}")
        if cached_entry and not cached_entry.is_expired:
            logger.debug(f"Returning cached value for key '{key}'")
            return cached_entry

        value = await value_supplier()
        entry = CacheEntry(key=key, value=value, ttl=ttl)
        await self.cache_service.set(entry)
        logger.debug(f"Cached value for key '{key}' with TTL {ttl} seconds")

        return entry