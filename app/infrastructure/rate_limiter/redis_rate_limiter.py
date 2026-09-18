# app/infrastructure/rate_limiter/redis_rate_limiter.py

from app.domain.ports.rate_limiter_port import RateLimiterPort


class RedisRateLimiter(RateLimiterPort):

    def __init__(self, redis_client):
        self.redis = redis_client

    async def increment(self, key: str, window_seconds: int) -> int:
        count = await self.redis.incr(key)

        if count == 1:
            await self.redis.expire(key, window_seconds)

        return count