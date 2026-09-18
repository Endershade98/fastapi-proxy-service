# app/domain/policies/rate_limit_policy.py

from dataclasses import dataclass
from app.domain.value_objects.request_quota import RequestQuota


@dataclass(frozen=True)
class RateLimitDecision:
    allowed: bool
    remaining: int
    retry_after_seconds: int


class RateLimitPolicy:

    def __init__(self, quota: RequestQuota):
        self._quota = quota

    def evaluate(self, current_count: int) -> RateLimitDecision:
        allowed = current_count <= self._quota.limit

        remaining = max(
            0,
            self._quota.limit - current_count
        )

        retry_after = 0 if allowed else self._quota.window_seconds

        return RateLimitDecision(
            allowed=allowed,
            remaining=remaining,
            retry_after_seconds=retry_after
        )

    @property
    def limit(self) -> int:
        return self._quota.limit

    @property
    def window_seconds(self) -> int:
        return self._quota.window_seconds