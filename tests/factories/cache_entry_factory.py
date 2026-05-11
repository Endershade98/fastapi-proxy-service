# tests/factories/cache_entry_factory.py

from datetime import datetime, timezone
from app.domain.value_objects.cache_entry import CacheEntry


def make_cache_entry(
    key: str = "user:1",
    value: dict = None,
    ttl_seconds: int = 60,
    created_at=None
) -> CacheEntry:
    return CacheEntry(
        key=key,
        value=value or {"ok": True},
        ttl_seconds=ttl_seconds,
        created_at=created_at or datetime.now(timezone.utc)
    )