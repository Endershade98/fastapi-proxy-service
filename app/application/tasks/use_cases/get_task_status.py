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
        self.task_reader = task_reader

    def execute(self, task_id: str) -> TaskStatusResult:

        result = self.task_reader.get_result(task_id)

        return TaskStatusResult(
            task_id=task_id,
            status=result.status,
            result=result.result if result.ready() else None
        )