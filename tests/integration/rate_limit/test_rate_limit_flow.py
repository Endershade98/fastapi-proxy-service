# tests/integration/rate_limit/test_rate_limit_flow.py

import pytest

from app.infrastructure.rate_limiter.redis_rate_limiter import (
    RedisRateLimiter,
)
from app.infrastructure.cache.redis_client import RedisClient


@pytest.mark.asyncio
async def test_rate_limiter_increments_counter():
    redis = RedisClient()
    limiter = RedisRateLimiter(redis_client=redis)

    key = "integration:test:rate-limit"

    try:
        first = await limiter.increment(
            key=key,
            window_seconds=60,
        )

        second = await limiter.increment(
            key=key,
            window_seconds=60,
        )

        assert first == 1
        assert second == 2

    finally:
        await redis.delete(key)
        await redis.close()