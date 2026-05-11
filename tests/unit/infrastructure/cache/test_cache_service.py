# tests/unit/infrastructure/cache/test_cache_service.py

import pytest
from app.infrastructure.cache.cache_service import CacheService


@pytest.mark.asyncio
async def test_cache_service_get_delegates():

    class FakeRedis:
        async def get(self, key):
            return "value"

    service = CacheService(FakeRedis())

    result = await service.get("k")

    assert result == "value"


@pytest.mark.asyncio
async def test_cache_service_set_delegates():

    called = {}

    class FakeRedis:
        async def set(self, entry):
            called["set"] = entry

    service = CacheService(FakeRedis())

    class FakeEntry:
        pass

    await service.set(FakeEntry())

    assert "set" in called