# app/domain/value_objects/request_quota.py

from dataclasses import dataclass

from app.domain.exceptions import InvalidQuotaError


@dataclass(frozen=True, slots=True)
class RequestQuota:
    """
    Value Object defining a request rate limit.
    """

    limit: int
    window_seconds: int

    def __post_init__(self) -> None:
        if self.limit <= 0 or self.window_seconds <= 0:
            raise InvalidQuotaError()