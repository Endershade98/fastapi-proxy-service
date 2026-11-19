# tests/integration/cache/test_redis_cache_flow.py

import pytest

from app.application.caching.models import CacheEntry
from app.infrastructure.cache.cache_service import CacheService
from app.infrastructure.cache.redis_client import RedisClient


@pytest.mark.asyncio
async def test_cache_roundtrip():
    redis = RedisClient()
    cache = CacheService(redis)

    key = "integration:test:cache"

    entry = CacheEntry(
        key=key,
        value={"a": 1},
        ttl_seconds=60,
        # aggiungi created_at se richiesto dal tuo modello
    )

    try:
        await cache.set(entry)

        result = await cache.get(key)

        assert result is not None
        assert result.key == key
        assert result.value == {"a": 1}
        assert result.ttl_seconds == 60

    finally:
        await cache.delete(key)
        await redis.close()