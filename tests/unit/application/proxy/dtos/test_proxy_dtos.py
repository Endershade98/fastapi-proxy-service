# tests/unit/application/proxy/dtos/test_proxy_dtos.py

import pytest

from app.application.proxy.dtos.request_dto import ProxyRequestDTO
from app.application.proxy.dtos.response_dto import ProxyResponseDTO


def test_proxy_request_dto():
    request = ProxyRequestDTO(
        url="https://example.com",
        ttl_seconds=60,
    )

    assert request.url == "https://example.com"
    assert request.ttl_seconds == 60


def test_proxy_request_dto_default_ttl():
    request = ProxyRequestDTO(
        url="https://example.com",
    )

    assert request.ttl_seconds == 60


def test_proxy_request_rejects_empty_url():
    with pytest.raises(ValueError):
        ProxyRequestDTO(url="")


@pytest.mark.parametrize("ttl", [0, -1])
def test_proxy_request_rejects_invalid_ttl(ttl):
    with pytest.raises(ValueError):
        ProxyRequestDTO(
            url="https://example.com",
            ttl_seconds=ttl,
        )


def test_proxy_request_is_immutable():
    request = ProxyRequestDTO(
        url="https://example.com",
    )

    with pytest.raises(AttributeError):
        request.url = "https://other.com"


def test_proxy_response_dto():
    response = ProxyResponseDTO(
        url="https://example.com",
        data={"ok": True},
        from_cache=False,
    )

    assert response.url == "https://example.com"
    assert response.data == {"ok": True}
    assert response.from_cache is False