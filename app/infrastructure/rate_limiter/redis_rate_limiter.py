# app/infrastructure/rate_limiter/redis_rate_limiter.py
from app.domain.services.rate_limiter_interface import RateLimiterInterface


class RedisRateLimiter:

    def __init__(self, redis_client):
        self.redis = redis_client

    async def increment(self, key: str, window: int) -> int:
        count = await self.redis.incr(key)

        if count == 1:
            await self.redis.expire(key, window)

        return count