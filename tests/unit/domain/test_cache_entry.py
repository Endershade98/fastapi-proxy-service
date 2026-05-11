# tests/unit/domain/test_cache_entry.py

import pytest
from app.domain.entities.cache_entry import CacheEntry

def test_cache_entry_creation():
    entry = CacheEntry(key="test", value={"a": 1}, ttl=60)
    assert entry.key == "test"
    assert entry.value == {"a": 1}
    assert entry.ttl == 60

def test_cache_entry_immutable():
    entry = CacheEntry(key="test", value=123, ttl=30)
    with pytest.raises(AttributeError):
        entry.key = "new_key"