# app/interfaces/api/schemas/tasks.py

from pydantic import BaseModel


class TaskStatusResponseSchema(BaseModel):
    task_id: str
    status: str
    result: dict | None

    @classmethod
    def from_result(cls, result):
        return cls(
            task_id=result.task_id,
            status=result.status,
            result=result.result
        )