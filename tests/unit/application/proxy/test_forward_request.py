# tests/unit/application/proxy/test_forward_request.py

import pytest
from unittest.mock import AsyncMock

from app.application.proxy.use_cases.forward_request import ForwardRequestUseCase
from app.application.proxy.dtos.request_dto import ProxyRequestDTO


@pytest.mark.asyncio
async def test_forward_request_uses_cache():

    cache_use_case = AsyncMock()
    remote = AsyncMock()

    cache_use_case.execute.return_value = type(
        "R",
        (),
        {"value": "cached", "from_cache": True}
    )()

    use_case = ForwardRequestUseCase(cache_use_case, remote)

    result = await use_case.execute(
        ProxyRequestDTO(url="http://test", ttl_seconds=60)
    )

    assert result.from_cache is True
    assert result.data == "cached"