# tests/unit/application/security/test_enforce_rate_limit.py

import pytest
from unittest.mock import AsyncMock

from app.application.security.use_cases.enforce_rate_limit import EnforceRateLimitUseCase
from app.domain.policies.rate_limit_policy import RateLimitPolicy
from app.domain.value_objects.request_quota import RequestQuota


@pytest.mark.asyncio
async def test_rate_limit_allows_request():

    repo = AsyncMock()
    repo.increment.return_value = 1

    policy = RateLimitPolicy(
        RequestQuota(
            limit=5,
            window_seconds=60
        )
    )

    use_case = EnforceRateLimitUseCase(
        repository=repo,
        policy=policy
    )

    result = await use_case.execute("client-1")

    assert result.allowed is True
    assert result.limit == 5
    assert result.remaining == 4