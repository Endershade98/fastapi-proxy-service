# tests/unit/application/tasks/use_cases/test_get_task_status.py

from app.application.tasks.use_cases.get_task_status import (
    GetTaskStatusUseCase,
)
from app.application.tasks import TaskResult, TaskStatus


class FakeTaskReader:
    def __init__(self, result: TaskResult):
        self.result = result
        self.calls = []

    def get(self, task_id: str) -> TaskResult:
        self.calls.append(task_id)
        return self.result


def test_returns_pending_task():
    reader = FakeTaskReader(
        TaskResult(
            task_id="task-1",
            status=TaskStatus.PENDING,
            result=None,
            ready=False,
        )
    )

    use_case = GetTaskStatusUseCase(
        task_reader=reader,
    )

    result = use_case.execute("task-1")

    assert result.task_id == "task-1"
    assert result.status == "pending"
    assert result.result is None

    assert reader.calls == ["task-1"]


def test_returns_started_task():
    reader = FakeTaskReader(
        TaskResult(
            task_id="task-1",
            status=TaskStatus.STARTED,
            result=None,
            ready=False,
        )
    )

    use_case = GetTaskStatusUseCase(
        task_reader=reader,
    )

    result = use_case.execute("task-1")

    assert result.status == "started"
    assert result.result is None


def test_returns_success_result():
    reader = FakeTaskReader(
        TaskResult(
            task_id="task-1",
            status=TaskStatus.SUCCESS,
            result={"value": 42},
            ready=True,
        )
    )

    use_case = GetTaskStatusUseCase(
        task_reader=reader,
    )

    result = use_case.execute("task-1")

    assert result.task_id == "task-1"
    assert result.status == "success"
    assert result.result == {"value": 42}


def test_does_not_expose_result_when_task_is_not_ready():
    reader = FakeTaskReader(
        TaskResult(
            task_id="task-1",
            status=TaskStatus.FAILURE,
            result={"secret": "should-not-be-returned"},
            ready=False,
        )
    )

    use_case = GetTaskStatusUseCase(
        task_reader=reader,
    )

    result = use_case.execute("task-1")

    assert result.status == "failure"
    assert result.result is None


def test_preserves_task_id():
    reader = FakeTaskReader(
        TaskResult(
            task_id="abc-123",
            status=TaskStatus.SUCCESS,
            result="done",
            ready=True,
        )
    )

    use_case = GetTaskStatusUseCase(
        task_reader=reader,
    )

    result = use_case.execute("abc-123")

    assert result.task_id == "abc-123"