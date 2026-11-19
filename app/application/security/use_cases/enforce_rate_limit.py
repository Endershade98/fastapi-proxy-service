# app/application/security/use_cases/enforce_rate_limit.py

from dataclasses import dataclass

from app.application.ports.rate_limiter import RateLimiterPort
from app.application.security.dtos.rate_limit_result import (
    RateLimitResult,
)
from app.domain.policies.rate_limit_policy import RateLimitPolicy


@dataclass
class EnforceRateLimitUseCase:
    repository: RateLimiterPort
    policy: RateLimitPolicy

    async def execute(self, key: str) -> RateLimitResult:
        count = await self.repository.increment(
            key=key,
            window_seconds=self.policy.window_seconds,
        )

        decision = self.policy.evaluate(count)

        return RateLimitResult(
            allowed=decision.allowed,
            limit=self.policy.limit,
            remaining=decision.remaining,
            retry_after_seconds=decision.retry_after_seconds,
        )