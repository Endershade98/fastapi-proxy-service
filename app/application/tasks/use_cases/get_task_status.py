# app/application/tasks/use_cases/get_task_status.py

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TaskStatusResult:
    task_id: str
    status: str
    result: Any | None


class GetTaskStatusUseCase:

    def __init__(self, task_reader):
        self._reader = task_reader

    def execute(self, task_id: str) -> TaskStatusResult:

        task = self._reader.get_result(task_id)

        return TaskStatusResult(
            task_id=task_id,
            status=task.status,
            result=task.result if task.ready() else None
        )