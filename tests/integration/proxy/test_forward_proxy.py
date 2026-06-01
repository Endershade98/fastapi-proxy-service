# tests/integration/proxy/test_forward_proxy.py

import pytest
from app.application.proxy.use_cases.forward_proxy_request import ForwardProxyRequestUseCase


class FakeRemote:
    async def fetch(self, url):
        return {"data": "ok"}


class FakeCacheUseCase:
    async def execute(self, key, supplier, ttl_seconds):
        class R:
            value = {"data": "ok"}
            from_cache = False
        return R()


@pytest.mark.asyncio
async def test_forward_proxy():
    uc = ForwardProxyRequestUseCase(
        remote_resource=FakeRemote(),
        cache_use_case=FakeCacheUseCase(),
    )

    result = await uc.execute("http://test.com")

    assert result.data == {"data": "ok"}