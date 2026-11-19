# app/infrastructure/cache/cache_service.py

from app.application.caching.models import CacheEntry
from app.application.ports.cache import CachePort
from app.infrastructure.cache.redis_client import RedisClient


class CacheService(CachePort):

    def __init__(self, redis: RedisClient):
        self._redis = redis

    async def get(self, key: str) -> CacheEntry | None:
        return await self._redis.get(key)

    async def set(self, entry: CacheEntry) -> None:
        await self._redis.set(entry)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)