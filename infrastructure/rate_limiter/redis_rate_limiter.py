# infrastructure/rate_limiter/redis_rate_limiter.py
from app.domain.services.rate_limiter_interface import RateLimiterInterface


class RedisRateLimiter(RateLimiterInterface):
    def __init__(self, redis):
        self.redis = redis

    async def allow(self, request) -> bool:
        key = f"rate_limit:{request.client.host}"
        count = await self.redis.incr(key)

        if count == 1:
            await self.redis.expire(key, 60)

        return count <= 10