import pytest
from app.services.proxy_service import ProxyService


class TestProxyFlow:

    url = "https://test.com"

    @pytest.mark.asyncio
    async def test_cache_hit(self, mocker):
        service = ProxyService()

        # mock cache
        mocker.patch("app.services.proxy_service.cache.get", return_value={"cached": True})

        result = await service.forward_request(self.url)

        assert result["cached"] is True