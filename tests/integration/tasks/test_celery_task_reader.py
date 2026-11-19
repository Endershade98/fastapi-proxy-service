# tests/integration/tasks/test_celery_task_reader.py

import pytest

from app.application.tasks import TaskStatus
from app.infrastructure.celery.celery_app import celery_app
from app.infrastructure.tasks.celery_task_reader import (
    CeleryTaskReader,
)


def test_reads_pending_task():
    reader = CeleryTaskReader(celery_app)

    result = reader.get("task-that-does-not-exist")

    assert result.task_id == "task-that-does-not-exist"
    assert result.status == TaskStatus.PENDING
    assert result.ready is False