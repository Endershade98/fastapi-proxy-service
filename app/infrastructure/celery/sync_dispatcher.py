# app/infrastructure/celery/sync_dispatcher.py

from app.domain.entities.cache_entry import CacheEntry


class SyncTaskDispatcher:

    def __init__(self, cache_service):
        self.cache_service = cache_service

    async def dispatch_cache_set(self, key, value, ttl):
        entry = CacheEntry(
            key=key,
            value=value,
            ttl=ttl
        )
        await self.cache_service.set(entry)