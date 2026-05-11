# tests/unit/infrastructure/test_mongo_logger.py

from unittest.mock import patch
from app.infrastructure.logging.mongo_logger import MongoLogger
from app.domain.events.log_event import LogEvent


def test_mongo_logger_dispatches_celery_task():

    logger = MongoLogger()

    event = LogEvent(
        event_type="TEST",
        message="hello"
    )

    with patch("app.infrastructure.celery.tasks.log_tasks.log_event_task.delay") as mock_task:

        import asyncio
        asyncio.run(logger.log(event))

        mock_task.assert_called_once()