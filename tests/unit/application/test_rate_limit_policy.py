# tests/unit/application/test_rate_limit_policy.py

from app.domain.policies.rate_limit_policy import RateLimitPolicy
from app.domain.value_objects.request_quota import RequestQuota


def test_rate_limit_allowed():
    policy = RateLimitPolicy(RequestQuota(limit=10, window_seconds=60))
    result = policy.evaluate(5)

    assert result.allowed is True
    assert result.remaining == 5


def test_rate_limit_exceeded():
    policy = RateLimitPolicy(RequestQuota(limit=10, window_seconds=60))
    result = policy.evaluate(15)

    assert result.allowed is False
    assert result.remaining == 0