# app/interfaces/api/routes/tasks.py

from fastapi import APIRouter, Depends

from app.bootstrap.container import get_task_status_use_case

router = APIRouter()


@router.get("/{task_id}")
async def task_status(
    task_id: str,
    use_case=Depends(get_task_status_use_case)
):

    result = use_case.execute(task_id)

    return {
        "task_id": result.task_id,
        "status": result.status,
        "result": result.result
    }