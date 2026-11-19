# tests/unit/application/proxy/use_cases/test_forward_proxy_request.py

import pytest

from app.application.proxy.dtos.request_dto import ProxyRequestDTO
from app.application.proxy.use_cases.forward_proxy_request import (
    ForwardProxyRequestUseCase,
)


class FakeRemoteResource:
    def __init__(self, value):
        self.value = value
        self.calls = []

    async def fetch(self, url: str):
        self.calls.append(url)
        return self.value


class FakeCacheUseCase:
    def __init__(self, value, from_cache=False):
        self.value = value
        self.from_cache = from_cache
        self.calls = []

    async def execute(self, key, supplier, ttl_seconds):
        self.calls.append(
            {
                "key": key,
                "ttl_seconds": ttl_seconds,
            }
        )

        class Result:
            pass

        result = Result()
        result.value = self.value
        result.from_cache = self.from_cache

        return result


@pytest.mark.asyncio
async def test_forwards_request_and_returns_response():
    remote = FakeRemoteResource(
        {"data": "ok"},
    )

    cache = FakeCacheUseCase(
        {"data": "ok"},
        from_cache=False,
    )

    use_case = ForwardProxyRequestUseCase(
        remote_resource=remote,
        cache_use_case=cache,
    )

    request = ProxyRequestDTO(
        url="https://example.com",
        ttl_seconds=30,
    )

    result = await use_case.execute(request)

    assert result.url == "https://example.com"
    assert result.data == {"data": "ok"}
    assert result.from_cache is False

    assert cache.calls == [
        {
            "key": "https://example.com",
            "ttl_seconds": 30,
        }
    ]


@pytest.mark.asyncio
async def test_returns_cached_response():
    remote = FakeRemoteResource(
        {"remote": True},
    )

    cache = FakeCacheUseCase(
        {"cached": True},
        from_cache=True,
    )

    use_case = ForwardProxyRequestUseCase(
        remote_resource=remote,
        cache_use_case=cache,
    )

    request = ProxyRequestDTO(
        url="https://example.com",
        ttl_seconds=60,
    )

    result = await use_case.execute(request)

    assert result.data == {"cached": True}
    assert result.from_cache is True


@pytest.mark.asyncio
async def test_passes_supplier_to_cache_use_case():
    remote = FakeRemoteResource(
        {"remote": True},
    )

    cache = FakeCacheUseCase(
        {"cached": True},
    )

    use_case = ForwardProxyRequestUseCase(
        remote_resource=remote,
        cache_use_case=cache,
    )

    request = ProxyRequestDTO(
        url="https://example.com",
        ttl_seconds=60,
    )

    await use_case.execute(request)

    # The use case must delegate loading to the cache abstraction.
    assert cache.calls[0]["key"] == request.url