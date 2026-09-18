# app/interfaces/api/schemas/tasks.py

from pydantic import BaseModel
from typing import Any


class TaskStatusResponseSchema(BaseModel):
    task_id: str
    status: str
    result: Any | None

    @classmethod
    def from_result(cls, result):
        return cls(
            task_id=result.task_id,
            status=result.status,
            result=result.result
        )