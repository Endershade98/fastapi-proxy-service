# app/domain/value_objects/request_quota.py

from dataclasses import dataclass


@dataclass(frozen=True)
class RequestQuota:
    limit: int
    period: int

    def __post_init__(self):
        if self.limit <= 0:
            raise ValueError("limit must be > 0")

        if self.period <= 0:
            raise ValueError("period must be > 0")