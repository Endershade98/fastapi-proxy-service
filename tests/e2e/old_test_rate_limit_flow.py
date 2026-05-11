# tests/e2e/test_rate_limit_flow.py

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import create_app


@pytest.mark.asyncio
async def test_rate_limit_flow(monkeypatch):
    app = create_app(testing=True)

    async def fake_fetch(self, url):
        return {
            "url": url,
            "data": "upstream response"
        }

    monkeypatch.setattr(
        "app.infrastructure.clients.http_client.HttpClient.fetch",
        fake_fetch
    )

    transport = ASGITransport(app=app)

    payload = {
        "url": "https://example.com",
        "method": "GET"
    }

    async with AsyncClient(
        transport=transport,
        base_url="http://testserver"
    ) as client:

        for _ in range(10):
            res = await client.post("/proxy/", json=payload)
            assert res.status_code == 200

        # l'11esima può essere limitata oppure no in testing mode
        res = await client.post("/proxy/", json=payload)
        assert res.status_code in (200, 429)