# app/application/proxy/dtos/request_dto.py

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProxyRequestDTO:
    url: str
    ttl_seconds: int = 60

    def __post_init__(self) -> None:
        if not self.url:
            raise ValueError("url is required")

        if self.ttl_seconds <= 0:
            raise ValueError(
                "ttl_seconds must be greater than zero"
            )