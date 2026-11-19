# app/infrastructure/rate_limiter/redis_rate_limiter.py

from app.application.ports.rate_limiter import RateLimiterPort


class RedisRateLimiter(RateLimiterPort):

    def __init__(self, redis_client):
        self._redis = redis_client

    async def increment(
        self,
        key: str,
        window_seconds: int,
    ) -> int:

        count = await self._redis.incr(key)

        if count == 1:
            await self._redis.expire(
                key,
                window_seconds,
            )

        return count