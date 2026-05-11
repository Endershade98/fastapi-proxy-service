# tests/integration/cache/test_redis_client.py

import pytest
from datetime import datetime, timezone
from app.infrastructure.cache.redis_client import RedisClient
from app.domain.value_objects.cache_entry import CacheEntry


@pytest.mark.asyncio
async def test_cache_set_calls_redis(monkeypatch):

    called = {}

    class FakeRedis:
        async def set(self, *args, **kwargs):
            called["set"] = True

        async def get(self, key):
            return None

    client = RedisClient()
    client.redis = FakeRedis()

    entry = CacheEntry(
        key="k",
        value={"a": 1},
        ttl_seconds=60,
        created_at=datetime.now(timezone.utc)
    )

    await client.set(entry)

    assert called["set"] is True


@pytest.mark.asyncio
async def test_cache_get_returns_none(monkeypatch):

    class FakeRedis:
        async def get(self, key):
            return None

    client = RedisClient()
    client.redis = FakeRedis()

    result = await client.get("missing")

    assert result is None