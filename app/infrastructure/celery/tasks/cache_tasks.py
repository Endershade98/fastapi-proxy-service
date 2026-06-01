# app/infrastructure/celery/tasks/cache_tasks.py

from app.infrastructure.celery.celery_app import celery_app
from app.infrastructure.cache.redis_client import RedisClient
from app.domain.value_objects.cache_entry import CacheEntry


@celery_app.task(name="save_cache")
def save_cache_task(payload: dict):

    import asyncio

    async def run():

        client = RedisClient()

        await client.set(
            CacheEntry(
                key=payload["key"],
                value=payload["value"],
                ttl_seconds=payload.get("ttl", 60),
            )
        )

    asyncio.run(run())