# tests/integration/cache/test_cache_entry.py

import pytest
from datetime import datetime, timedelta
from app.domain.entities.cache_entry import CacheEntry

def test_cache_entry_immutable():
    entry = CacheEntry(key="k", value={"a":1})
    with pytest.raises(Exception):
        entry.key = "new"

def test_cache_entry_expired():
    entry = CacheEntry(key="k", value={"a":1}, ttl=1)
    assert not entry.is_expired