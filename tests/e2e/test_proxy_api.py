# tests/e2e/test_proxy_api.py

def test_proxy_endpoint(client):
    response = client.post(
        "/proxy/",
        json={
            "url": "https://example.com",
            "ttl": 60
        }
    )

    assert response.status_code in (200, 502)

    if response.status_code == 200:
        data = response.json()
        assert "data" in data
        assert "from_cache" in data