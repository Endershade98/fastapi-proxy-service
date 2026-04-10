# app/domain/services/rate_limit_policy.py
class RateLimitPolicy:

    def __init__(self, limit: int):
        self.limit = limit

    def is_allowed(self, count: int) -> bool:
        return count <= self.limit