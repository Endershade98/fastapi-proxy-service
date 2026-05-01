# app/domain/services/rate_limit_policy.py

from app.domain.value_objects.request_quota import RequestQuota


class RateLimitPolicy:

    def __init__(self, quota: RequestQuota):
        self.quota = quota

    def is_allowed(self, count: int) -> bool:
        return count <= self.quota.limit

    def get_limit(self) -> int:
        return self.quota.limit

    def get_period(self) -> int:
        return self.quota.period