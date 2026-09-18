# tests/integration/cache/test_redis_cache_flow.py

import pytest
from app.infrastructure.cache.redis_client import RedisClient
from app.domain.value_objects.cache_entry import CacheEntry


@pytest.mark.asyncio
async def test_cache_roundtrip():
    redis = RedisClient()

    entry = CacheEntry(key="test", value={"a": 1}, ttl_seconds=60)

    await redis.set(entry)
    result = await redis.get("test")

    assert result is not None
    assert result.value == {"a": 1}