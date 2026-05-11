# tests/unit/domain/test_cache_entry.py

from datetime import datetime, timezone, timedelta
import pytest

from app.domain.value_objects.cache_entry import CacheEntry
from app.domain.exceptions import InvalidTTLError


def test_should_create_valid_cache_entry():
    entry = CacheEntry(
        key="abc",
        value={"name": "john"},
        ttl_seconds=60
    )

    assert entry.key == "abc"
    assert entry.is_valid is True


def test_should_be_expired_when_time_passed():
    created_at = datetime.now(timezone.utc) - timedelta(seconds=120)

    entry = CacheEntry(
        key="abc",
        value={"x": 1},
        ttl_seconds=60,
        created_at=created_at
    )

    assert entry.is_expired is True
    assert entry.is_valid is False


def test_should_compute_expiration_date():
    created_at = datetime.now(timezone.utc)

    entry = CacheEntry(
        key="abc",
        value={},
        ttl_seconds=60,
        created_at=created_at
    )

    assert entry.expires_at == created_at + timedelta(seconds=60)


def test_should_reject_invalid_ttl():
    with pytest.raises(InvalidTTLError):
        CacheEntry(
            key="abc",
            value={},
            ttl_seconds=0
        )