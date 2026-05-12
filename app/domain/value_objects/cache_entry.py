# app/domain/value_objects/cache_entry.py

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any
from app.domain.exceptions import InvalidTTLError


@dataclass(frozen=True)
class CacheEntry:
    key: str
    value: Any
    ttl_seconds: int | None = None
    created_at: datetime | None = None

    def __post_init__(self):
        if self.ttl_seconds is not None and self.ttl_seconds <= 0:
            raise InvalidTTLError()
        if self.created_at is None:
            object.__setattr__(self, "created_at", datetime.now(timezone.utc))

    @property
    def expires_at(self) -> datetime | None:
        if self.ttl_seconds is None:
            return None
        return self.created_at + timedelta(seconds=self.ttl_seconds)

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def is_valid(self) -> bool:
        return not self.is_expired