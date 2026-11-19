# app/domain/events/rate_limit.py

from dataclasses import dataclass
from datetime import datetime

from app.domain.value_objects.client_ip import ClientIP
from app.domain.value_objects.request_quota import RequestQuota


@dataclass(frozen=True, slots=True)
class RateLimitExceeded:
    """
    Domain event raised when a request exceeds the configured quota.
    """

    client_ip: ClientIP
    quota: RequestQuota
    occurred_at: datetime