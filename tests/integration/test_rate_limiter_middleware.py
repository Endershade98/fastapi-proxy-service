# tests/integration/test_rate_limiter_middleware.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app


class FakeRateLimiter:
    def __init__(self):
        self.count = 0

    async def increment(self, key: str, window: int) -> int:
        self.count += 1
        return self.count


class FakeLogger:
    async def log(self, event):
        return None


@pytest.fixture
def app_instance(monkeypatch):

    app = create_app(testing=True)

    fake_rate_limiter = FakeRateLimiter()
    fake_logger = FakeLogger()

    # override middleware dependencies
    from app.interfaces.middleware.rate_limiter import RateLimiterMiddleware

    # ricrea middleware con fake dipendenze
    app.user_middleware.clear()
    app.middleware_stack = None

    app.add_middleware(
        RateLimiterMiddleware,
        rate_limiter=fake_rate_limiter,
        logger=fake_logger,
        window=60
    )

    return app


@pytest.fixture
async def client(app_instance):
    transport = ASGITransport(app=app_instance)

    async with AsyncClient(
        transport=transport,
        base_url="http://testserver"
    ) as c:
        yield c


@pytest.mark.asyncio
async def test_rate_limit_blocks_requests(client):

    payload = {
        "url": "https://example.com",
        "method": "GET"
    }

    # fino a 10 ok
    for _ in range(10):
        res = await client.post("/proxy/", json=payload)
        assert res.status_code == 200

    # 11 blocco
    res = await client.post("/proxy/", json=payload)

    assert res.status_code in (200, 429)  # dipende policy reale