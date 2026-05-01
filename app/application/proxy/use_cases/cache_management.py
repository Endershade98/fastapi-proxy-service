# app/application/proxy/use_cases/cache_management.py

from app.domain.value_objects.cache_entry import CacheEntry
from app.application.proxy.dtos.cache_result import CacheResult


class CacheManager:
    def __init__(self, cache_service):
        self.cache_service = cache_service

    async def get_or_set(self, key: str, value_supplier, ttl: int = 60) -> CacheResult:
        cached = await self.cache_service.get(key)

        if cached and not cached.is_expired:
            return CacheResult(
                value=cached.value,
                from_cache=True
            )

        value = await value_supplier()

        entry = CacheEntry(key=key, value=value, ttl=ttl)
        await self.cache_service.set(entry)

        return CacheResult(
            value=value,
            from_cache=False
        )