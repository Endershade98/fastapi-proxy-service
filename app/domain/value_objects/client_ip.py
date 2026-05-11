# app/domain/value_objects/client_ip.py

import ipaddress
from dataclasses import dataclass
from app.domain.exceptions import InvalidIPError


@dataclass(frozen=True)
class ClientIP:
    value: str

    def __post_init__(self):
        try:
            normalized = str(ipaddress.ip_address(self.value))
            object.__setattr__(self, "value", normalized)
        except ValueError:
            raise InvalidIPError(self.value)

    def __str__(self) -> str:
        return self.value