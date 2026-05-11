# app/infrastructure/celery/tasks/cache_tasks.py

import asyncio

from app.infrastructure.celery.celery_app import celery_app
from app.infrastructure.cache.redis_client import RedisClient
from app.domain.value_objects.cache_entry import CacheEntry


@celery_app.task(name="save_cache_task")
def save_cache_task(key, value, ttl):

    async def run():
        client = RedisClient()

        entry = CacheEntry(
            key=key,
            value=value,
            ttl=ttl
        )

        await client.set(entry)

    asyncio.run(run())