# app/domain/entities/cached_resource.py

from dataclasses import dataclass
from typing import Any


@dataclass
class CachedResource:
    key: str
    value: Any