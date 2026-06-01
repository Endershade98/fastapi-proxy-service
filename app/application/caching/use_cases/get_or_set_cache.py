# app/application/caching/use_cases/get_or_set_cache.py

from dataclasses import dataclass
from typing import Callable, Awaitable, Any

from app.domain.value_objects.cache_entry import CacheEntry
from app.domain.ports.cache_port import CachePort
from app.application.proxy.dtos.cache_result import CacheResult


@dataclass
class GetOrSetCacheUseCase:

    def __init__(self, cache: CachePort):
        self._cache = cache

    async def execute(
        self,
        key: str,
        supplier: Callable[[], Awaitable[Any]],
        ttl_seconds: int = 60
    ) -> CacheResult[Any]:

        cached = await self._cache.get(key)

        if cached and cached.is_valid:
            return CacheResult(value=cached.value, from_cache=True)

        value = await supplier()

        await self._cache.set(
            CacheEntry(
                key=key,
                value=value,
                ttl_seconds=ttl_seconds
            )
        )

        return CacheResult(value=value, from_cache=False)