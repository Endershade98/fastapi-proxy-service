# app/domain/exceptions.py

class DomainException(Exception):
    """Base exception for domain errors."""
    pass


class InvalidIPError(DomainException):
    def __init__(self, ip: str):
        super().__init__(f"Invalid IP address: {ip}")


class InvalidQuotaError(DomainException):
    def __init__(self):
        super().__init__("Quota values must be greater than zero")


class QuotaExceededError(DomainException):
    def __init__(self):
        super().__init__("Quota exceeded")


class CacheExpiredError(DomainException):
    def __init__(self):
        super().__init__("Cache entry expired")


class InvalidTTLError(DomainException):
    def __init__(self):
        super().__init__("TTL must be greater than zero")