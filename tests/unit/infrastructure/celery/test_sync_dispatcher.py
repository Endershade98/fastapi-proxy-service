# tests/unit/infrastructure/celery/test_sync_dispatcher.py

import pytest
from app.infrastructure.celery.sync_dispatcher import SyncTaskDispatcher


@pytest.mark.asyncio
async def test_sync_dispatcher_calls_cache_service(mocker):

    cache_mock = mocker.AsyncMock()

    dispatcher = SyncTaskDispatcher(cache_mock)

    await dispatcher.dispatch_cache_set("k", {"a": 1}, 60)

    cache_mock.set.assert_called_once()