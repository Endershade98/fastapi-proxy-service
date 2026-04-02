import json
from app.cache.redis_client import redis_client

class CacheService:

    async def get(self, key: str):
        value = await redis_client.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: dict, ttl: int = 60):
        await redis_client.set(key, json.dumps(value), ex=ttl)

