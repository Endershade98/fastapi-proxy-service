# app/domain/value_objects/request_quota.py
from dataclasses import dataclass

@dataclass(frozen=True)
class RequestQuota:
    limit: int
    window_seconds: int

    def is_exceeded(self, count: int) -> bool:
        return count > self.limit