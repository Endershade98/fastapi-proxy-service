# tests/e2e/test_rate_limit_flow.py

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app


@pytest.mark.asyncio
async def test_rate_limit_flow():

    app = create_app(testing=True)
    transport = ASGITransport(app=app)

    payload = {
        "url": "https://example.com",
        "method": "GET"
    }

    async with AsyncClient(
        transport=transport,
        base_url="http://testserver"
    ) as client:

        # entro limite (FakeRateLimiter → sempre OK)
        for _ in range(10):
            res = await client.post("/proxy/", json=payload)
            assert res.status_code == 200

        # il fake limiter può anche NON bloccare mai → se vuoi testare block,
        # devi controllarlo esplicitamente (vedi sotto test dedicato)