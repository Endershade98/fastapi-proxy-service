# app/domain/value_objects/client_ip.py

import ipaddress
from dataclasses import dataclass

from app.domain.exceptions import InvalidIPError


@dataclass(frozen=True, slots=True)
class ClientIP:
    """
    Value Object representing a normalized client IP address.

    The object guarantees that the contained value is a valid
    IPv4 or IPv6 address.
    """

    value: str

    def __post_init__(self) -> None:
        try:
            normalized = str(ipaddress.ip_address(self.value))
        except ValueError as exc:
            raise InvalidIPError(self.value) from exc

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value