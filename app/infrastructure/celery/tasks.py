from app.infrastructure.celery.celery_app import celery_app
from app.cache.cache_service import CacheService

cache_service = CacheService()

@celery_app.task
def async_save_cache(key: str, value: dict, ttl: int = 60):
    import asyncio
    asyncio.run(cache_service.set(key, value, ttl))