# app/interfaces/api/routes/tasks.py

from fastapi import APIRouter, Depends

from app.bootstrap.container import get_task_status_use_case
from app.application.tasks.use_cases.get_task_status import GetTaskStatusUseCase
from app.interfaces.api.schemas.tasks import TaskStatusResponseSchema

router = APIRouter()


@router.get("/{task_id}", response_model=TaskStatusResponseSchema)
def task_status(
    task_id: str,
    use_case: GetTaskStatusUseCase = Depends(get_task_status_use_case)
):
    result = use_case.execute(task_id)

    return TaskStatusResponseSchema.from_result(result)