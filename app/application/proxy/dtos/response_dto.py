# app/application/proxy/dtos/response_dto.py

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProxyResponseDTO:
    data: Any
    from_cache: bool