# app/domain/entities/cache_entry.py
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta

@dataclass(frozen=True)
class CacheEntry:
    key: str
    value: dict
    ttl: int = 60
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_valid(self) -> bool:
        return not self.is_expired

    @property
    def is_expired(self) -> bool:
        now = datetime.now(timezone.utc)  # ora timezone-aware
        return now > self.created_at + timedelta(seconds=self.ttl)