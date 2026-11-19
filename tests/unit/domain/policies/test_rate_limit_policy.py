# tests/unit/domain/policies/test_rate_limit_policy.py

import pytest

from app.domain.policies.rate_limit_policy import (
    RateLimitDecision,
    RateLimitPolicy,
)
from app.domain.value_objects.request_quota import RequestQuota


@pytest.fixture
def policy() -> RateLimitPolicy:
    return RateLimitPolicy(
        RequestQuota(
            limit=100,
            window_seconds=60,
        )
    )


def test_allows_request_when_count_is_zero(policy: RateLimitPolicy):
    decision = policy.evaluate(0)

    assert decision == RateLimitDecision(
        allowed=True,
        remaining=100,
        retry_after_seconds=0,
    )


def test_allows_request_at_limit(policy: RateLimitPolicy):
    decision = policy.evaluate(100)

    assert decision.allowed is True
    assert decision.remaining == 0
    assert decision.retry_after_seconds == 0


def test_rejects_request_above_limit(policy: RateLimitPolicy):
    decision = policy.evaluate(101)

    assert decision.allowed is False
    assert decision.remaining == 0
    assert decision.retry_after_seconds == 60


def test_remaining_decreases_with_request_count(
    policy: RateLimitPolicy,
):
    decision = policy.evaluate(25)

    assert decision.allowed is True
    assert decision.remaining == 75
    assert decision.retry_after_seconds == 0


def test_remaining_never_becomes_negative(
    policy: RateLimitPolicy,
):
    decision = policy.evaluate(150)

    assert decision.remaining == 0


def test_negative_count_is_rejected(
    policy: RateLimitPolicy,
):
    with pytest.raises(ValueError):
        policy.evaluate(-1)


def test_exposes_limit(policy: RateLimitPolicy):
    assert policy.limit == 100


def test_exposes_window_seconds(policy: RateLimitPolicy):
    assert policy.window_seconds == 60