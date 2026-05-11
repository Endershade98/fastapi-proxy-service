# app/domain/exceptions.py

class DomainException(Exception):
    pass

class InvalidIPError(DomainException):
    pass

class QuotaExceededError(DomainException):
    pass

class CacheExpiredError(DomainException):
    pass