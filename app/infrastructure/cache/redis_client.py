# app/infrastructure/cache/redis_client.py
import json
from datetime import datetime
import redis.asyncio as redis
from app.config.settings import settings
from app.domain.value_objects.cache_entry import CacheEntry

class RedisClient:
    def __init__(self):
        self.redis_port = settings.REDIS_PORT
        self.redis_host = settings.REDIS_HOST
        self.redis_url = f"redis://{self.redis_host}:{self.redis_port}"
        self.redis = redis.from_url(self.redis_url)

    async def get(self, key: str) -> CacheEntry | None:
        raw_value = await self.redis.get(key)
        if raw_value is None:
            return None

        try:
            data = json.loads(raw_value)
            created_at = None
            if data.get("created_at"):
                # parse ISO string in datetime
                created_at = datetime.fromisoformat(data["created_at"])
            return CacheEntry(
                key=key,
                value=data.get("value"),
                ttl=data.get("ttl", 60),
                created_at=created_at
            )
        except (json.JSONDecodeError, TypeError, AttributeError, ValueError):
            return None

    async def set(self, entry: CacheEntry):
        value_to_store = {
            "value": entry.value,
            "ttl": entry.ttl,
            "created_at": entry.created_at.isoformat() if entry.created_at else datetime.utcnow().isoformat()
        }
        await self.redis.set(entry.key, json.dumps(value_to_store), ex=entry.ttl)

    async def incr(self, key: str) -> int:
        return await self.redis.incr(key)

    async def expire(self, key: str, seconds: int):
        await self.redis.expire(key, seconds)
    
# instance
redis_client = RedisClient()