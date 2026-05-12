# tests/unit/infrastructure/celery/test_sync_dispatcher.py

from app.infrastructure.celery.sync_dispatcher import SyncTaskDispatcher


def test_sync_dispatcher_executes_task():
    dispatcher = SyncTaskDispatcher()

    def fake_task(data):
        return data["x"] + 1

    result = dispatcher.dispatch(fake_task, {"x": 1})

    assert result == 2