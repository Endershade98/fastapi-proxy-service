# app/infrastructure/cache/cache_service.py

from app.domain.ports.cache_port import CachePort
from app.domain.value_objects.cache_entry import CacheEntry
from app.infrastructure.cache.redis_client import RedisClient


class CacheService(CachePort):

    def __init__(self, redis: RedisClient):
        self.redis = redis

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, entry):
        await self.redis.set(entry)

    async def delete(self, key: str):
        await self.redis.delete(key)

    # BRIDGE FOR RATE LIMITER (TEMP CLEANUP)
    async def incr(self, key: str) -> int:
        return await self.redis.incr(key)

    async def expire(self, key: str, seconds: int):
        return await self.redis.expire(key, seconds)