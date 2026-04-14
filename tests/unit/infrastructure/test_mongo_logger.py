# tests/unit/infrastructure/test_mongo_logger.py
import pytest
from unittest.mock import AsyncMock
from app.infrastructure.logging.mongo_logger import MongoLogger
from app.domain.events.log_event import LogEvent


@pytest.mark.asyncio
async def test_mongo_logger():
    collection_mock = AsyncMock()

    logger = MongoLogger(collection=collection_mock)

    event = LogEvent(event_type="TEST_EVENT", message="Test message")

    await logger.log(event)

    collection_mock.insert_one.assert_called_once_with(event.to_dict())