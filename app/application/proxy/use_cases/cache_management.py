# app/application/proxy/use_cases/cache_management.py

from typing import Callable, Awaitable, Any

from app.application.proxy.dtos.cache_result import CacheResult
from app.domain.entities.cache_entry import CacheEntry
from app.domain.services.cache_service_interface import CacheServiceInterface
from app.domain.services.task_dispatcher_interface import TaskDispatcherInterface


class GetOrSetCacheUseCase:

    def __init__(
        self,
        cache_service: CacheServiceInterface,
        dispatcher: TaskDispatcherInterface | None = None
    ):
        self.cache_service = cache_service
        self.dispatcher = dispatcher

    async def get_or_set(
        self,
        key: str,
        value_supplier: Callable[[], Awaitable[Any]],
        ttl: int = 60
    ) -> CacheResult:

        cached = await self.cache_service.get(key)

        if cached and not cached.is_expired:
            return CacheResult(
                value=cached.value,
                from_cache=True
            )

        value = await value_supplier()

        if self.dispatcher:
            await self.dispatcher.dispatch_cache_set(key, value, ttl)
        else:
            await self.cache_service.set(
                CacheEntry(key=key, value=value, ttl=ttl)
            )

        return CacheResult(
            value=value,
            from_cache=False
        )