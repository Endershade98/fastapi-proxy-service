# app/domain/services/rate_limit_policy.py

from app.domain.value_objects.client_ip import ClientIP
from app.domain.value_objects.request_quota import RequestQuota

class RateLimitPolicy:

    def __init__(self, limit: int):
        self.limit = limit

    def is_allowed(self, count: int) -> bool:
        return count <= self.limit