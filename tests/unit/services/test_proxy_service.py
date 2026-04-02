import pytest
from app.services.proxy_service import ProxyService

class TestProxyService:

    @pytest.mark.asyncio
    async def test_proxy_service_basic(self, mocker):
        service = ProxyService()

        # 🔹 MOCK CACHE
        mocker.patch("app.services.proxy_service.cache.get", return_value=None)
        mocker.patch("app.services.proxy_service.cache.set", return_value=None)

        # 🔹 MOCK HTTP
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "ok"}

        mocker.patch("app.services.proxy_service.fetch", return_value=mock_response)

        result = await service.forward_request("https://fake-url.com")

        assert result["status_code"] == 200
        assert result["data"]["test"] == "ok"