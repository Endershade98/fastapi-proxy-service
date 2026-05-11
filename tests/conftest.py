# tests/conftest.py

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app
from app.bootstrap.dummies import DummyRateLimiter, DummyLogger


@pytest.fixture
def app_instance():
    return create_app(
        testing=True,
        rate_limiter=DummyRateLimiter(),
        logger=DummyLogger()
    )


@pytest.fixture
async def client(app_instance):
    transport = ASGITransport(app=app_instance)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client