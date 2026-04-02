import pytest

class TestProxyAPI:

    url = "https://jsonplaceholder.typicode.com/todos/1"
    route = "/proxy/"

    @pytest.mark.asyncio
    async def test_proxy_success(self, client):
        response = await client.post(
            self.route,
            json={"url": self.url}
    )

        assert response.status_code == 200
        data = response.json()
        assert "status_code" in data
        assert "data" in data