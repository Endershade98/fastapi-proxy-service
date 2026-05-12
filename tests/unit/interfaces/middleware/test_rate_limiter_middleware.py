# tests/unit/interfaces/middleware/test_rate_limiter_middleware.py

import pytest
from fastapi import FastAPI, Request
from starlette.responses import Response
from httpx import AsyncClient, ASGITransport

from app.interfaces.middleware.rate_limiter import RateLimiterMiddleware


class FakeRateLimiter:
    async def is_allowed(self, ip: str):
        return ip != "1.1.1.1"


class FakeLogger:
    async def log_event(self, *args, **kwargs):
        pass


async def endpoint(request: Request):
    return Response("OK", status_code=200)


@pytest.mark.asyncio
async def test_rate_limiter_allows_request():

    app = FastAPI()

    app.add_middleware(
        RateLimiterMiddleware,
        rate_limiter=FakeRateLimiter(),
        logger=FakeLogger()
    )

    @app.get("/")
    async def route(request: Request):
        return await endpoint(request)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert response.text == "OK"