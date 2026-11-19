# tests/unit/application/caching/test_get_or_set_cache.py

from datetime import datetime, timezone

import pytest

from app.application.caching.models import CacheEntry
from app.application.caching.use_cases.get_or_set_cache import (
    GetOrSetCacheUseCase,
)


class FakeCache:
    def __init__(self):
        self.entries: dict[str, CacheEntry] = {}
        self.get_calls = []
        self.set_calls = []

    async def get(self, key: str):
        self.get_calls.append(key)
        return self.entries.get(key)

    async def set(self, entry: CacheEntry):
        self.set_calls.append(entry)
        self.entries[entry.key] = entry

    async def delete(self, key: str):
        self.entries.pop(key, None)


@pytest.mark.asyncio
async def test_returns_cached_value_without_calling_supplier():
    cache = FakeCache()

    cache.entries["key"] = CacheEntry(
        key="key",
        value={"cached": True},
        ttl_seconds=60,
        created_at=datetime.now(timezone.utc),
    )

    use_case = GetOrSetCacheUseCase(cache=cache)

    supplier_called = False

    async def supplier():
        nonlocal supplier_called
        supplier_called = True
        return {"cached": False}

    result = await use_case.execute(
        key="key",
        supplier=supplier,
        ttl_seconds=60,
    )

    assert result.value == {"cached": True}
    assert result.from_cache is True
    assert supplier_called is False

    assert cache.get_calls == ["key"]
    assert cache.set_calls == []


@pytest.mark.asyncio
async def test_calls_supplier_on_cache_miss():
    cache = FakeCache()

    use_case = GetOrSetCacheUseCase(cache=cache)

    async def supplier():
        return {"value": 123}

    result = await use_case.execute(
        key="key",
        supplier=supplier,
        ttl_seconds=60,
    )

    assert result.value == {"value": 123}
    assert result.from_cache is False

    assert cache.get_calls == ["key"]
    assert len(cache.set_calls) == 1

    stored = cache.set_calls[0]

    assert stored.key == "key"
    assert stored.value == {"value": 123}
    assert stored.ttl_seconds == 60


@pytest.mark.asyncio
async def test_supplier_is_called_only_once_on_single_execution():
    cache = FakeCache()
    use_case = GetOrSetCacheUseCase(cache=cache)

    calls = 0

    async def supplier():
        nonlocal calls
        calls += 1
        return "value"

    await use_case.execute(
        key="key",
        supplier=supplier,
        ttl_seconds=60,
    )

    assert calls == 1


@pytest.mark.asyncio
async def test_propagates_supplier_exception():
    cache = FakeCache()
    use_case = GetOrSetCacheUseCase(cache=cache)

    async def supplier():
        raise RuntimeError("remote service failed")

    with pytest.raises(RuntimeError, match="remote service failed"):
        await use_case.execute(
            key="key",
            supplier=supplier,
            ttl_seconds=60,
        )

    assert cache.set_calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize("ttl", [0, -1])
async def test_rejects_invalid_ttl(ttl):
    cache = FakeCache()
    use_case = GetOrSetCacheUseCase(cache=cache)

    async def supplier():
        return "value"

    with pytest.raises(ValueError):
        await use_case.execute(
            key="key",
            supplier=supplier,
            ttl_seconds=ttl,
        )