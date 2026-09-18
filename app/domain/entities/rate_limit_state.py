# app/domain/entities/rate_limit_state.py

from dataclasses import dataclass


@dataclass
class RateLimitState:
    key: str
    count: int