# tests/unit/application/security/use_cases/test_enforce_rate_limit.py

import pytest

from app.application.security.use_cases.enforce_rate_limit import (
    EnforceRateLimitUseCase,
)
from app.domain.policies.rate_limit_policy import RateLimitPolicy
from app.domain.value_objects.request_quota import RequestQuota


class FakeRateLimiter:
    def __init__(self, count: int):
        self.count = count
        self.calls = []

    async def increment(self, key: str, window_seconds: int) -> int:
        self.calls.append(
            {
                "key": key,
                "window_seconds": window_seconds,
            }
        )
        return self.count


@pytest.fixture
def policy():
    return RateLimitPolicy(
        RequestQuota(
            limit=100,
            window_seconds=60,
        )
    )


@pytest.mark.asyncio
async def test_allows_request(policy):
    limiter = FakeRateLimiter(count=1)

    use_case = EnforceRateLimitUseCase(
        rate_limiter=limiter,
        policy=policy,
    )

    result = await use_case.execute("client:127.0.0.1")

    assert result.allowed is True
    assert result.limit == 100
    assert result.remaining == 99
    assert result.retry_after_seconds == 0
    assert result.window_seconds == 60

    assert limiter.calls == [
        {
            "key": "client:127.0.0.1",
            "window_seconds": 60,
        }
    ]


@pytest.mark.asyncio
async def test_rejects_request_when_limit_is_exceeded(policy):
    limiter = FakeRateLimiter(count=101)

    use_case = EnforceRateLimitUseCase(
        rate_limiter=limiter,
        policy=policy,
    )

    result = await use_case.execute("client:127.0.0.1")

    assert result.allowed is False
    assert result.limit == 100
    assert result.remaining == 0
    assert result.retry_after_seconds == 60
    assert result.window_seconds == 60


@pytest.mark.asyncio
async def test_request_at_exact_limit_is_allowed(policy):
    limiter = FakeRateLimiter(count=100)

    use_case = EnforceRateLimitUseCase(
        rate_limiter=limiter,
        policy=policy,
    )

    result = await use_case.execute("client:127.0.0.1")

    assert result.allowed is True
    assert result.remaining == 0


@pytest.mark.asyncio
async def test_passes_correct_window_to_port(policy):
    limiter = FakeRateLimiter(count=1)

    use_case = EnforceRateLimitUseCase(
        rate_limiter=limiter,
        policy=policy,
    )

    await use_case.execute("client:127.0.0.1")

    assert limiter.calls[0]["window_seconds"] == 60