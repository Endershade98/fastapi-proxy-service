# app/infrastructure/cache/redis_client.py

import json
from datetime import datetime

import redis.asyncio as redis

from app.config.settings import settings
from app.domain.entities.cache_entry import CacheEntry


class RedisClient:

    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)

    async def get(self, key: str) -> CacheEntry | None:
        raw = await self.redis.get(key)

        if raw is None:
            return None

        try:
            data = json.loads(raw)

            return CacheEntry(
                key=key,
                value=data["value"],
                ttl=data["ttl"],
                created_at=datetime.fromisoformat(data["created_at"])
            )

        except Exception:
            return None

    async def set(self, entry: CacheEntry):

        payload = {
            "value": entry.value,
            "ttl": entry.ttl,
            "created_at": entry.created_at.isoformat()
        }

        await self.redis.set(
            entry.key,
            json.dumps(payload),
            ex=entry.ttl
        )

    async def incr(self, key: str) -> int:
        return await self.redis.incr(key)

    async def expire(self, key: str, seconds: int):
        await self.redis.expire(key, seconds)