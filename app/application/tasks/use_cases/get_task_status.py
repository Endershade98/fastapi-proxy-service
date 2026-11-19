# app/application/tasks/use_cases/get_task_status.py

from dataclasses import dataclass
from typing import Any

from app.application.ports.task_reader import TaskReaderPort


@dataclass(frozen=True, slots=True)
class TaskStatusResult:
    task_id: str
    status: str
    result: Any | None


class GetTaskStatusUseCase:

    def __init__(self, task_reader: TaskReaderPort):
        self._reader = task_reader

    def execute(self, task_id: str) -> TaskStatusResult:
        if not task_id:
            raise ValueError("task_id is required")

        task = self._reader.get_result(task_id)

        status = str(task.status).lower()

        return TaskStatusResult(
            task_id=task_id,
            status=status,
            result=task.result if task.ready() else None,
        )