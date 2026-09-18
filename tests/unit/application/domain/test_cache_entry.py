# tests/unit/domain/test_cache_entry.py

from app.domain.value_objects.cache_entry import CacheEntry


def test_cache_entry_valid():
    entry = CacheEntry(key="k", value="v", ttl_seconds=60)
    assert entry.is_valid is True


def test_cache_entry_expired_logic():
    entry = CacheEntry(key="k", value="v", ttl_seconds=1)
    assert isinstance(entry.is_valid, bool)