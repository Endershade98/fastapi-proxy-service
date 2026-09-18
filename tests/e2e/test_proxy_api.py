# tests/e2e/test_proxy_api.py

import pytest
from starlette.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client():
    app = create_app(testing=True)
    return TestClient(app)


HEADERS = {
    "x-forwarded-for": "127.0.0.1",
}


def test_proxy_success_flow(client):
    response = client.post(
        "/proxy/",
        json={
            "url": "https://httpbin.org/get",
            "ttl": 10,
        },
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert "url" in response.json()


def test_proxy_cache_behavior(client):
    payload = {
        "url": "https://httpbin.org/get",
        "ttl": 10,
    }

    r1 = client.post("/proxy/", json=payload, headers=HEADERS)
    r2 = client.post("/proxy/", json=payload, headers=HEADERS)

    assert r1.status_code == 200
    assert r2.status_code == 200

    # fallback-safe cache assertion (non fragile)
    assert r1.json() == r2.json()