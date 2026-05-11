# app/infrastructure/celery/tasks/log_tasks.py

from app.infrastructure.celery.celery_app import celery_app
from app.infrastructure.db.mongodb import get_logs_collection


@celery_app.task(name="log_event_task")
def log_event_task(event: dict):

    collection = get_logs_collection()

    import asyncio

    async def _insert():
        await collection.insert_one(event)

    try:
        asyncio.run(_insert())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_insert())