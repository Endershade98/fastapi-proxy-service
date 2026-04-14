# app/domain/services/rate_limit_policy.py
class RateLimitPolicy:

    def __init__(self, limit: int, period: int):
        self.limit = limit
        self.period = period

    def is_allowed(self, count: int) -> bool:
        return count <= self.limit
    
    def get_period(self) -> int:
        return self.period
    
    def get_limit(self) -> int:
        return self.limit