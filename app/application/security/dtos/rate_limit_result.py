# app/application/security/dtos/rate_limit_result.py

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RateLimitResult:
    allowed: bool
    limit: int
    remaining: int
    retry_after_seconds: int