# app/application/security/use_cases/enforce_rate_limit.py

from app.application.security.dtos.rate_limit_result import RateLimitResult
from app.domain.services.rate_limit_policy import RateLimitPolicy
from app.domain.repositories.rate_limiter_repository import RateLimiterInterface


class EnforceRateLimitUseCase:

    def __init__(
        self,
        repository: RateLimiterInterface,
        policy: RateLimitPolicy
    ):
        self.repository = repository
        self.policy = policy

    async def execute(self, key: str) -> RateLimitResult:

        count = await self.repository.increment(
            key,
            self.policy.get_period()
        )

        allowed = self.policy.is_allowed(count)

        remaining = max(
            self.policy.get_limit() - count,
            0
        )

        return RateLimitResult(
            allowed=allowed,
            limit=self.policy.get_limit(),
            remaining=remaining
        )