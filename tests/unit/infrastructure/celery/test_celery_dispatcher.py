# tests/unit/infrastructure/celery/test_celery_dispatcher.py

from app.infrastructure.celery.celery_dispatcher import CeleryTaskDispatcher


class FakeTask:
    def delay(self, *args, **kwargs):
        return "ok"


def test_celery_dispatcher_dispatch(monkeypatch):
    dispatcher = CeleryTaskDispatcher()

    monkeypatch.setattr(dispatcher, "_get_task", lambda name: FakeTask())

    result = dispatcher.dispatch("test-task", {"a": 1})

    assert result == "ok"