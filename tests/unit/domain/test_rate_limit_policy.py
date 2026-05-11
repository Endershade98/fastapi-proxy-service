# tests/unit/domain/test_rate_limit_policy.py

from app.domain.policies.rate_limit_policy import RateLimitPolicy
from app.domain.value_objects.request_quota import RequestQuota


def test_should_allow_when_under_limit():
    policy = RateLimitPolicy(
        RequestQuota(limit=5, window_seconds=60)
    )

    result = policy.evaluate(current_count=3)

    assert result.allowed is True
    assert result.remaining == 2
    assert result.retry_after_seconds == 0


def test_should_allow_when_equal_limit():
    policy = RateLimitPolicy(
        RequestQuota(limit=5, window_seconds=60)
    )

    result = policy.evaluate(current_count=5)

    assert result.allowed is True
    assert result.remaining == 0


def test_should_block_when_over_limit():
    policy = RateLimitPolicy(
        RequestQuota(limit=5, window_seconds=60)
    )

    result = policy.evaluate(current_count=6)

    assert result.allowed is False
    assert result.remaining == 0
    assert result.retry_after_seconds == 60