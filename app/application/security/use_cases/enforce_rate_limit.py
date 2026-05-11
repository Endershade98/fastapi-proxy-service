# app/application/security/use_cases/enforce_rate_limit.py

from app.application.security.dtos.rate_limit_result import RateLimitResult
from app.domain.policies.rate_limit_policy import RateLimitPolicy
from app.domain.ports.rate_limiter_port import RateLimiterPort


class EnforceRateLimitUseCase:

    def __init__(
        self,
        repository: RateLimiterPort,
        policy: RateLimitPolicy
    ):
        self._repository = repository
        self._policy = policy

    async def execute(self, key: str) -> RateLimitResult:

        count = await self._repository.increment(
            key=key,
            window_seconds=self._policy.window_seconds
        )

        decision = self._policy.evaluate(count)

        return RateLimitResult(
            allowed=decision.allowed,
            limit=self._policy.limit,
            remaining=decision.remaining,
            retry_after_seconds=decision.retry_after_seconds
        )