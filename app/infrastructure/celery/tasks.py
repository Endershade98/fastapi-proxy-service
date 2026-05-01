# app/infrastructure/celery/tasks.py

from app.infrastructure.celery.celery_app import celery_app
from app.infrastructure.cache.cache_service import RedisCacheService
from app.domain.value_objects.cache_entry import CacheEntry


cache_service = RedisCacheService()

@celery_app.task
def async_save_cache(key: str, value: dict, ttl: int = 60):
    import asyncio
    entry = CacheEntry(key, value, ttl)
    asyncio.run(cache_service.set(entry))