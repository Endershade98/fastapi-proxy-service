# tests/integration/clients/test_http_client.py

import pytest
from app.infrastructure.clients.http_client import HttpClient


@pytest.mark.asyncio
async def test_http_fetch():

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"ok": True}

    class FakeClient:
        async def get(self, url):
            return FakeResponse()

    client = HttpClient()
    client.client = FakeClient()

    result = await client.fetch("http://test")

    assert result == {"ok": True}