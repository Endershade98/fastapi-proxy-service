# app/infrastructure/rate_limiter/redis_adapter.py
from app.infrastructure.cache.redis_client import RedisClient

class RedisAdapter:
    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client

    async def get(self, key: str):
        return await self.redis_client.get(key)

    async def set(self, key: str, value, ttl: int):
        await self.redis_client.set(key, value, ttl)