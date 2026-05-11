# tests/unit/infrastructure/logging/test_mongo_logger.py

import pytest
from unittest.mock import patch
import dataclasses

from app.infrastructure.logging.mongo_logger import MongoLogger
from app.domain.events.log_event import LogEvent


@pytest.mark.asyncio
async def test_mongo_logger_dispatches_celery_task():

    logger = MongoLogger()

    event = LogEvent(
        event_type="TEST",
        message="hello"
    )

    with patch(
        "app.infrastructure.celery.tasks.log_tasks.log_event_task.delay"
    ) as mock_task:

        await logger.log(event)

        assert mock_task.called