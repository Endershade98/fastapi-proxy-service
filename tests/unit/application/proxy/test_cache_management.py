# tests/unit/application/proxy/test_cache_management.py

import pytest
from unittest.mock import AsyncMock

from app.application.proxy.use_cases.cache_management import GetOrSetCacheUseCase
from app.domain.value_objects.cache_entry import CacheEntry


@pytest.mark.asyncio
async def test_cache_hit_returns_cached_value():

    cache = AsyncMock()
    dispatcher = AsyncMock()

    entry = CacheEntry(key="k", value={"x": 1}, ttl_seconds=60)

    cache.get.return_value = entry

    use_case = GetOrSetCacheUseCase(cache, dispatcher)

    result = await use_case.execute(
        key="k",
        supplier=AsyncMock(return_value={"x": 2}),
        ttl_seconds=60
    )

    assert result.from_cache is True
    assert result.value == {"x": 1}
    dispatcher.dispatch_cache_set.assert_not_called()

@pytest.mark.asyncio
async def test_cache_miss_stores_value():

    cache = AsyncMock()
    dispatcher = None

    cache.get.return_value = None

    use_case = GetOrSetCacheUseCase(cache, dispatcher)

    supplier = AsyncMock(return_value={"x": 10})

    result = await use_case.execute(
        key="k",
        supplier=supplier,
        ttl_seconds=60
    )

    assert result.from_cache is False
    assert result.value == {"x": 10}
    cache.set.assert_called_once()