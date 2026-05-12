# tests/unit/interfaces/api/test_proxy_endpoint.py

import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from app.interfaces.api.router import router


@pytest.mark.asyncio
async def test_proxy_endpoint_success(mocker):

    app = FastAPI()
    app.include_router(router)

    mock_use_case = mocker.AsyncMock()
    mock_use_case.execute.return_value = type(
        "Result",
        (),
        {
            "data": {"ok": True},
            "cached": False
        }
    )

    mocker.patch(
        "app.interfaces.api.routes.proxy.get_forward_request_use_case",
        return_value=lambda: mock_use_case
    )

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/proxy/",
            json={
                "url": "https://example.com",
                "ttl": 60
            }
        )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["ok"] is True
    assert body["cached"] is False