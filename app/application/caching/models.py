# app/application/caching/models.py

from dataclasses import dataclass
from datetime import datetime
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class CacheEntry(Generic[T]):
    """
    Application-level representation of a cached value.

    Expiration semantics are owned by the cache adapter.
    """

    key: str
    value: T
    ttl_seconds: int
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError("Cache key cannot be empty")

        if self.ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be greater than zero")


@dataclass(frozen=True, slots=True)
class CacheResult(Generic[T]):
    """
    Result returned by the cache use case.
    """

    value: T
    from_cache: bool