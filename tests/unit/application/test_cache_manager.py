# tests/unit/application/test_cache_manager.py
import pytest
from unittest.mock import AsyncMock

from app.application.proxy.use_cases.cache_management import CacheManager
from app.domain.value_objects.cache_entry import CacheEntry


@pytest.mark.asyncio
async def test_cache_manager_get_or_set_hit():

    mock_cache = AsyncMock()

    mock_cache.get.return_value = CacheEntry(
        key="k",
        value={"val": 1},
        ttl=60
    )

    manager = CacheManager(mock_cache)

    result = await manager.get_or_set("k", lambda: {"val": 2})

    assert result.value == {"val": 1}
    assert result.from_cache is True

    mock_cache.set.assert_not_awaited()


@pytest.mark.asyncio
async def test_cache_manager_get_or_set_miss():

    mock_cache = AsyncMock()
    mock_cache.get.return_value = None

    manager = CacheManager(mock_cache)

    async def supplier():
        return {"val": 2}

    result = await manager.get_or_set("k", supplier)

    assert result.value == {"val": 2}
    assert result.from_cache is False

    mock_cache.set.assert_awaited_once()