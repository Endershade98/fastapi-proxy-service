# tests/unit/application/proxy/test_retry_handler.py

import pytest
from unittest.mock import AsyncMock

from app.application.proxy.use_cases.retry_handler import RetryHandler


@pytest.mark.asyncio
async def test_retry_handler_delegates():

    dispatcher = AsyncMock()
    dispatcher.dispatch_retry.return_value = "task-id"

    handler = RetryHandler(dispatcher)

    result = await handler.execute("http://x")

    assert result == "task-id"
    dispatcher.dispatch_retry.assert_called_once()