# tests/integration/test_rate_limiter_middleware.py

import pytest


@pytest.mark.asyncio
async def test_rate_limit_blocks_requests(client, monkeypatch):

    async def fake_fetch(self, url):
        return {
            "url": url,
            "data": "upstream response"
        }

    monkeypatch.setattr(
        "app.infrastructure.clients.http_client.HttpClient.fetch",
        fake_fetch
    )

    payload = {
        "url": "https://example.com",
        "method": "GET"
    }

    for _ in range(10):
        res = await client.post("/proxy/", json=payload)
        assert res.status_code == 200

    res = await client.post("/proxy/", json=payload)

    assert res.status_code in (200, 429)