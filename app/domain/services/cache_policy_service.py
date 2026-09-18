# app/domain/services/cache_policy_service.py

from app.domain.value_objects.cache_entry import CacheEntry


class CachePolicyService:

    def should_refresh(self, entry: CacheEntry | None) -> bool:
        if entry is None:
            return True

        return entry.is_expired