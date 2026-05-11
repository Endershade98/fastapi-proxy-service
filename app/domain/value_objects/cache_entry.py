# app/domain/value_objects/cache_entry.py

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any
from app.domain.exceptions import InvalidTTLError


@dataclass(frozen=True)
class CacheEntry:
    key: str
    value: Any
    ttl_seconds: int = 60
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self):
        if self.ttl_seconds <= 0:
            raise InvalidTTLError()

    @property
    def expires_at(self) -> datetime:
        return self.created_at + timedelta(seconds=self.ttl_seconds)

    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def is_valid(self) -> bool:
        return not self.is_expired