# app/domain/services/rate_limit_service.py

from app.domain.policies.rate_limit_policy import (
    RateLimitPolicy,
    RateLimitDecision,
)


class RateLimitService:

    def __init__(self, policy: RateLimitPolicy):
        self._policy = policy

    def evaluate(self, current_count: int) -> RateLimitDecision:
        return self._policy.evaluate(current_count)