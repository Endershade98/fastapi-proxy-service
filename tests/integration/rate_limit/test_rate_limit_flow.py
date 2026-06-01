# tests/integration/rate_limit/test_rate_limit_flow.py

import pytest
from app.infrastructure.rate_limiter.redis_rate_limiter import RedisRateLimiter
from app.infrastructure.cache.redis_client import RedisClient


@pytest.mark.asyncio
async def test_rate_limit_increment():
    redis = RedisClient()
    limiter = RedisRateLimiter(redis)

    count = await limiter.increment("ip:test", 60)

    assert count >= 1