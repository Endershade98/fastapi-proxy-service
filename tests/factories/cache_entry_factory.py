# tests/factories/cache_entry_factory.py

from app.domain.entities.cache_entry import CacheEntry

def cache_entry_factory(
    key="test:key",
    value=None,
    ttl=60,
    hit=False
):
    if value is None:
        value = {"data": 123}

    entry = CacheEntry(key=key, value=value, ttl=ttl)

    # override frozen dataclass
    object.__setattr__(entry, "hit", hit)

    return entry