# app/application/proxy/dtos/request_dto.py

from dataclasses import dataclass


@dataclass(frozen=True)
class ProxyRequestDTO:
    url: str
    ttl: int = 60

    def __post_init__(self):
        if not self.url:
            raise ValueError("url required")

        if self.ttl <= 0:
            raise ValueError("ttl must be > 0")