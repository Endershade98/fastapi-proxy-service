# tests/unit/interfaces/api/test_tasks_endpoint.py

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.interfaces.api.router import router


@pytest.mark.asyncio
async def test_task_status_endpoint(mocker):

    app = FastAPI()
    app.include_router(router)

    mock_use_case = mocker.Mock()
    mock_use_case.execute.return_value = type(
        "Result",
        (),
        {
            "task_id": "123",
            "status": "done",
            "result": {"value": 42}
        }
    )

    mocker.patch(
        "app.interfaces.api.routes.tasks.get_task_status_use_case",
        return_value=lambda: mock_use_case
    )

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/tasks/123")

    assert response.status_code == 200

    body = response.json()

    assert body["task_id"] == "123"
    assert body["status"] == "done"
    assert body["result"]["value"] == 42