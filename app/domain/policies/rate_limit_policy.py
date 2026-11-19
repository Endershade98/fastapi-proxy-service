# app/domain/policies/rate_limit_policy.py

from dataclasses import dataclass

from app.domain.value_objects.request_quota import RequestQuota


@dataclass(frozen=True, slots=True)
class RateLimitDecision:
    """
    Result of evaluating the current rate-limit state.
    """

    allowed: bool
    remaining: int
    retry_after_seconds: int


class RateLimitPolicy:
    """
    Domain policy responsible for deciding whether a request
    is allowed according to a RequestQuota.
    """

    def __init__(self, quota: RequestQuota):
        self._quota = quota

    def evaluate(self, current_count: int) -> RateLimitDecision:
        if current_count < 0:
            raise ValueError(
                "current_count cannot be negative"
            )

        allowed = current_count <= self._quota.limit

        remaining = max(
            self._quota.limit - current_count,
            0,
        )

        retry_after_seconds = (
            0
            if allowed
            else self._quota.window_seconds
        )

        return RateLimitDecision(
            allowed=allowed,
            remaining=remaining,
            retry_after_seconds=retry_after_seconds,
        )

    @property
    def limit(self) -> int:
        return self._quota.limit

    @property
    def window_seconds(self) -> int:
        return self._quota.window_seconds