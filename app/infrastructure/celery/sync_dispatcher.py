# app/infrastructure/celery/sync_dispatcher.py

from app.domain.value_objects.cache_entry import CacheEntry


class SyncTaskDispatcher:

    def __init__(self, cache_service):
        self.cache_service = cache_service

    async def dispatch_cache_set(self, key: str, value: any, ttl: int) -> None:

        entry = CacheEntry(
            key=key,
            value=value
        )

        await self.cache_service.set(entry)