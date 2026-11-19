# app/domain/exceptions.py

class DomainException(Exception):
    """Base exception for all domain errors."""


class InvalidIPError(DomainException):
    def __init__(self, ip: str):
        super().__init__(f"Invalid IP address: {ip}")


class InvalidQuotaError(DomainException):
    def __init__(self):
        super().__init__(
            "Quota values must be greater than zero"
        )