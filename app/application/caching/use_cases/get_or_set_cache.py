# app/application/caching/use_cases/get_or_set_cache.py

from datetime import datetime, timezone
from typing import Any, Awaitable, Callable

from app.application.caching.models import (
    CacheEntry,
    CacheResult,
)
from app.application.ports.cache import CachePort


class GetOrSetCacheUseCase:
    """
    Application use case implementing cache-aside behavior.
    """

    def __init__(self, cache: CachePort):
        self._cache = cache

    async def execute(
        self,
        key: str,
        supplier: Callable[[], Awaitable[Any]],
        ttl_seconds: int = 60,
    ) -> CacheResult[Any]:

        cached = await self._cache.get(key)

        if cached is not None:
            return CacheResult(
                value=cached.value,
                from_cache=True,
            )

        value = await supplier()

        entry = CacheEntry(
            key=key,
            value=value,
            ttl_seconds=ttl_seconds,
            created_at=datetime.now(timezone.utc),
        )

        await self._cache.set(entry)

        return CacheResult(
            value=value,
            from_cache=False,
        )