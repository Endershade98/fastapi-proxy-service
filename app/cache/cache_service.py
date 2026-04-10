# app/infrastructure/cache/cache_service.py
from typing import Optional
from app.domain.services.cache_service_interface import CacheServiceInterface
from app.domain.entities.cache_entry import CacheEntry


class CacheService(CacheServiceInterface):

    def __init__(self, redis_client):
        self.redis = redis_client

    async def get(self, key: str) -> Optional[CacheEntry]:
        entry = await self.redis.get(key)

        if not entry:
            return None

        if entry.is_expired:
            return None

        return entry

    async def set(self, entry: CacheEntry) -> None:
        await self.redis.set(entry)