# app/infrastructure/celery/tasks/log_tasks.py

from app.infrastructure.celery.celery_app import celery_app
from app.infrastructure.db.mongodb import get_logs_collection


@celery_app.task(name="log_event_task")
def log_event_task(event: dict):
    """
    Async logging task executed by Celery worker.

    DDD rule:
    - infrastructure layer only
    - no domain logic
    - accepts primitive data (dict)
    """

    collection = get_logs_collection()

    # Motor async driver workaround:
    # Celery task is sync → use blocking insert via event loop safe call
    import asyncio

    async def _insert():
        await collection.insert_one(event)

    try:
        asyncio.run(_insert())
    except RuntimeError:
        # fallback if event loop already exists (rare in worker reuse)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_insert())