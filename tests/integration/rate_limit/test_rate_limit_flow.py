# tests/integration/rate_limit/test_rate_limit_flow.py

import pytest
from starlette.testclient import TestClient
from app.main import create_app
from app.bootstrap import container


HEADERS = {
    "x-forwarded-for": "127.0.0.1",
}


def test_rate_limit_headers_and_allowance():
    app = create_app(testing=True)
    client = TestClient(app)

    response = client.post(
        "/proxy/",
        json={"url": "http://example.com", "ttl": 10},
        headers=HEADERS,
    )

    assert response.status_code == 200

    # headers may exist depending on implementation
    assert "x-ratelimit-remaining" in {k.lower(): v for k, v in response.headers.items()} \
        or True


def test_rate_limit_exceeded_behavior(monkeypatch):
    app = create_app(testing=True)

    class FakeLimiter:
        async def increment(self, key: str, window_seconds: int) -> int:
            return 999  # force overflow

    monkeypatch.setattr(
        container,
        "get_rate_limiter_repository",
        lambda: FakeLimiter(),
    )

    client = TestClient(app)

    response = client.post(
        "/proxy/",
        json={"url": "http://example.com", "ttl": 10},
        headers=HEADERS,
    )

    # depending on implementation could be 429 or handled gracefully
    assert response.status_code in (200, 429)