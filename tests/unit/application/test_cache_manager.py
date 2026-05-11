# tests/unit/application/test_cache_manager.py

import pytest
from unittest.mock import AsyncMock

from app.application.proxy.use_cases.cache_management import GetOrSetCacheUseCase
from app.domain.entities.cache_entry import CacheEntry


@pytest.mark.asyncio
async def test_cache_manager_get_or_set_hit():
    mock_cache = AsyncMock()
    mock_dispatcher = AsyncMock()

    mock_cache.get.return_value = CacheEntry(
        key="k",
        value={"val": 1},
        ttl=60
    )

    manager = GetOrSetCacheUseCase(
        cache_service=mock_cache,
        dispatcher=mock_dispatcher
    )

    async def supplier():
        return {"val": 2}

    result = await manager.get_or_set("k", supplier)

    assert result.value == {"val": 1}
    assert result.from_cache is True

    mock_dispatcher.dispatch_cache_set.assert_not_awaited()
    mock_cache.set.assert_not_awaited()


@pytest.mark.asyncio
async def test_cache_manager_get_or_set_miss_dispatches_async_cache_set():
    mock_cache = AsyncMock()
    mock_dispatcher = AsyncMock()

    mock_cache.get.return_value = None

    manager = GetOrSetCacheUseCase(
        cache_service=mock_cache,
        dispatcher=mock_dispatcher
    )

    async def supplier():
        return {"val": 2}

    result = await manager.get_or_set("k", supplier)

    assert result.value == {"val": 2}
    assert result.from_cache is False

    mock_dispatcher.dispatch_cache_set.assert_awaited_once_with(
        "k",
        {"val": 2},
        60
    )

    mock_cache.set.assert_not_awaited()


@pytest.mark.asyncio
async def test_cache_manager_get_or_set_miss_without_dispatcher_falls_back_to_sync_set():
    mock_cache = AsyncMock()
    mock_cache.get.return_value = None

    manager = GetOrSetCacheUseCase(cache_service=mock_cache)

    async def supplier():
        return {"val": 2}

    result = await manager.get_or_set("k", supplier)

    assert result.value == {"val": 2}
    assert result.from_cache is False

    mock_cache.set.assert_awaited_once()