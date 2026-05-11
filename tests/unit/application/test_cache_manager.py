# tests/unit/application/test_cache_manager.py

import pytest
from unittest.mock import AsyncMock

from app.application.proxy.use_cases.cache_management import GetOrSetCacheUseCase
from app.domain.value_objects.cache_entry import CacheEntry


@pytest.mark.asyncio
async def test_cache_manager_get_or_set_hit():

    mock_cache = AsyncMock()
    mock_dispatcher = AsyncMock()

    mock_cache.get.return_value = CacheEntry(
        key="k",
        value={"val": 1},
        ttl_seconds=60
    )

    manager = GetOrSetCacheUseCase(
        cache_port=mock_cache,
        dispatcher=mock_dispatcher
    )

    result = await manager.execute(
        key="k",
        supplier=AsyncMock(return_value={"val": 2}),
        ttl_seconds=60
    )

    assert result.from_cache is True
    assert result.value == {"val": 1}

    mock_dispatcher.dispatch_cache_set.assert_not_called()


@pytest.mark.asyncio
async def test_cache_manager_get_or_set_miss_dispatches_async_cache_set():

    mock_cache = AsyncMock()
    mock_dispatcher = AsyncMock()

    mock_cache.get.return_value = None

    manager = GetOrSetCacheUseCase(
        cache_port=mock_cache,
        dispatcher=mock_dispatcher
    )

    supplier = AsyncMock(return_value={"val": 2})

    result = await manager.execute(
        key="k",
        supplier=supplier,
        ttl_seconds=60
    )

    assert result.from_cache is False
    assert result.value == {"val": 2}

    mock_dispatcher.dispatch_cache_set.assert_called_once()

@pytest.mark.asyncio
async def test_cache_manager_get_or_set_miss_without_dispatcher_falls_back_to_sync_set():

    mock_cache = AsyncMock()
    mock_cache.get.return_value = None

    manager = GetOrSetCacheUseCase(
        cache_port=mock_cache
    )

    supplier = AsyncMock(return_value={"val": 3})

    result = await manager.execute(
        key="k",
        supplier=supplier,
        ttl_seconds=60
    )

    assert result.from_cache is False
    assert result.value == {"val": 3}

    mock_cache.set.assert_called_once()