# tests/e2e/test_proxy_flow.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app


@pytest.mark.asyncio
async def test_proxy_endpoint():

    app = create_app(testing=True)
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://testserver"
    ) as client:

        res = await client.post("/proxy/", json={
            "url": "https://example.com",
            "method": "GET"
        })

        assert res.status_code == 200

        body = res.json()

        assert body["data"] == {
            "url": "https://example.com",
            "data": "upstream response"
        }

        assert body["cached"] in (True, False)