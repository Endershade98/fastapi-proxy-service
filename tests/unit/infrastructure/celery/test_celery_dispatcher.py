# tests/unit/infrastructure/celery/test_celery_dispatcher.py

import pytest
from app.infrastructure.celery.celery_dispatcher import CeleryTaskDispatcher


@pytest.mark.asyncio
async def test_dispatch_cache_set_calls_delay(mocker):

    mock_task = mocker.patch(
        "app.infrastructure.celery.tasks.cache_tasks.save_cache_task.delay"
    )

    dispatcher = CeleryTaskDispatcher()

    await dispatcher.dispatch_cache_set("k", {"a": 1}, 60)

    mock_task.assert_called_once_with("k", {"a": 1}, 60)