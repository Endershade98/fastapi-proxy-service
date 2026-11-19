# tests/unit/application/caching/test_models.py

from datetime import datetime, timezone

import pytest

from app.application.caching.models import CacheEntry, CacheResult


def test_cache_entry_is_created():
    created_at = datetime.now(timezone.utc)

    entry = CacheEntry(
        key="test-key",
        value={"foo": "bar"},
        ttl_seconds=60,
        created_at=created_at,
    )

    assert entry.key == "test-key"
    assert entry.value == {"foo": "bar"}
    assert entry.ttl_seconds == 60
    assert entry.created_at == created_at


def test_cache_entry_rejects_empty_key():
    with pytest.raises(ValueError):
        CacheEntry(
            key="",
            value="value",
            ttl_seconds=60,
            created_at=datetime.now(timezone.utc),
        )


def test_cache_entry_rejects_non_positive_ttl():
    for ttl in (0, -1):
        with pytest.raises(ValueError):
            CacheEntry(
                key="test",
                value="value",
                ttl_seconds=ttl,
                created_at=datetime.now(timezone.utc),
            )

"""
def test_cache_entry_requires_timezone_aware_datetime():
    with pytest.raises(ValueError):
        CacheEntry(
            key="test",
            value="value",
            ttl_seconds=60,
            created_at=datetime.now(),
        )
"""

def test_cache_entry_is_immutable():
    entry = CacheEntry(
        key="test",
        value="value",
        ttl_seconds=60,
        created_at=datetime.now(timezone.utc),
    )

    with pytest.raises(AttributeError):
        entry.key = "other"


def test_cache_result_from_cache():
    result = CacheResult(
        value={"foo": "bar"},
        from_cache=True,
    )

    assert result.value == {"foo": "bar"}
    assert result.from_cache is True


def test_cache_result_not_from_cache():
    result = CacheResult(
        value={"foo": "bar"},
        from_cache=False,
    )

    assert result.from_cache is False