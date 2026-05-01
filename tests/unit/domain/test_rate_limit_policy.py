# tests/unit/domain/test_rate_limit_policy.py

from app.domain.services.rate_limit_policy import RateLimitPolicy
from app.domain.value_objects.request_quota import RequestQuota


def test_rate_limit_policy():
    quota = RequestQuota(limit=10, period=60)
    policy = RateLimitPolicy(quota)

    assert policy.get_limit() == 10
    assert policy.get_period() == 60

    assert policy.is_allowed(5) is True
    assert policy.is_allowed(10) is True
    assert policy.is_allowed(11) is False