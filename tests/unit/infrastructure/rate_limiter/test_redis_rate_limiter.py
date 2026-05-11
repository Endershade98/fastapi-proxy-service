# tests/integration/rate_limiter/test_redis_rate_limiter.py

import pytest
from app.infrastructure.rate_limiter.redis_rate_limiter import RedisRateLimiter


@pytest.mark.asyncio
async def test_increment_sets_expire(monkeypatch):

    class FakeRedis:
        def __init__(self):
            self.calls = {}

        async def incr(self, key):
            self.calls["incr"] = key
            return 1

        async def expire(self, key, window):
            self.calls["expire"] = (key, window)

    redis = FakeRedis()
    limiter = RedisRateLimiter(redis)

    result = await limiter.increment("k", 60)

    assert result == 1
    assert redis.calls["incr"] == "k"
    assert redis.calls["expire"] == ("k", 60)