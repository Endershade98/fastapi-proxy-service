# app/application/proxy/dtos/cache_result.py

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class CacheResult(Generic[T]):
    value: T
    from_cache: bool