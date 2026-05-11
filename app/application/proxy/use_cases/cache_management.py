# app/application/proxy/use_cases/cache_management.py

from typing import Callable, Awaitable, Any

from app.application.proxy.dtos.cache_result import CacheResult
from app.domain.value_objects.cache_entry import CacheEntry
from app.domain.ports.cache_port import CachePort
from app.domain.ports.task_dispatcher_port import TaskDispatcherPort


class GetOrSetCacheUseCase:

    def __init__(
        self,
        cache_port: CachePort,
        dispatcher: TaskDispatcherPort | None = None
    ):
        self._cache = cache_port
        self._dispatcher = dispatcher

    async def execute(
        self,
        key: str,
        supplier: Callable[[], Awaitable[Any]],
        ttl_seconds: int = 60
    ) -> CacheResult[Any]:

        cached = await self._cache.get(key)

        if cached and cached.is_valid:
            return CacheResult(
                value=cached.value,
                from_cache=True
            )

        value = await supplier()

        if self._dispatcher:
            await self._dispatcher.dispatch_cache_set(
                key=key,
                value=value,
                ttl_seconds=ttl_seconds
            )
        else:
            await self._cache.set(
                CacheEntry(
                    key=key,
                    value=value,
                    ttl_seconds=ttl_seconds
                )
            )

        return CacheResult(
            value=value,
            from_cache=False
        )