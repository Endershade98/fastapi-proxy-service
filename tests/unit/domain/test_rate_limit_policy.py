# tests/unit/domain/test_rate_limit_policy.py
from app.domain.services.rate_limit_policy import RateLimitPolicy

def test_rate_limit_policy():
    policy = RateLimitPolicy(limit=10, period=60)
    
    assert policy.get_limit() == 10
    assert policy.get_period() == 60

    assert policy.is_allowed(5) is True
    assert policy.is_allowed(10) is True

    assert policy.is_allowed(11) is False