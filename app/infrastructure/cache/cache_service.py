# app/infrastructure/cache/cache_service.py

from app.domain.ports.cache_port import CachePort
from app.domain.value_objects.cache_entry import CacheEntry
from app.infrastructure.cache.redis_client import RedisClient


class CacheService(CachePort):

    def __init__(self, redis: RedisClient):
        self.redis = redis

    async def get(self, key: str) -> CacheEntry | None:
        return await self.redis.get(key)

    async def set(self, entry: CacheEntry) -> None:
        await self.redis.set(entry)