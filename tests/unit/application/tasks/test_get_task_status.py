# tests/unit/application/tasks/test_get_task_status.py

from app.application.tasks.use_cases.get_task_status import GetTaskStatusUseCase


class FakeTask:
    def __init__(self):
        self.status = "done"
        self.result = {"ok": True}

    def ready(self):
        return True


class FakeReader:
    def get_result(self, task_id):
        return FakeTask()


def test_get_task_status():

    use_case = GetTaskStatusUseCase(FakeReader())

    result = use_case.execute("123")

    assert result.task_id == "123"
    assert result.status == "done"
    assert result.result == {"ok": True}