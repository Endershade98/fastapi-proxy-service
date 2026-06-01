# tests/unit/application/test_cache_use_case.py

import pytest
from app.application.caching.use_cases.get_or_set_cache import GetOrSetCacheUseCase
from app.domain.value_objects.cache_entry import CacheEntry


class FakeCache:
    def __init__(self):
        self.store = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, entry):
        self.store[entry.key] = entry


@pytest.mark.asyncio
async def test_cache_miss_then_set():
    cache = FakeCache()
    uc = GetOrSetCacheUseCase(cache)

    async def supplier():
        return "value"

    result = await uc.execute("key", supplier, ttl_seconds=60)

    assert result.from_cache is False
    assert result.value == "value"