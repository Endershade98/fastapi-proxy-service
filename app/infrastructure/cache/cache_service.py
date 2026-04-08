# app/infrastructure/cache/cache_service.py
from app.domain.services.cache_service_interface import CacheServiceInterface
from app.domain.value_objects.cache_entry import CacheEntry
from app.infrastructure.cache.redis_client import RedisClient

class CacheService(CacheServiceInterface):
    def __init__(self, redis: RedisClient):
        self.redis = redis

    def get(self, key: str) -> CacheEntry | None:
        data = self.redis.get(key)
        if data:
            return CacheEntry.deserialize(data)
        return None

    def set(self, entry: CacheEntry) -> None:
        self.redis.set(entry.key, entry.serialize(), entry.ttl)