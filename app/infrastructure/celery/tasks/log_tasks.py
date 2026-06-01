# app/infrastructure/celery/tasks/log_tasks.py

import asyncio

from app.infrastructure.celery.celery_app import (
    celery_app
)

from app.infrastructure.db.mongodb import (
    get_logs_collection
)


@celery_app.task(name="log_event_task")
def log_event_task(event_type: str, message: str, **kwargs):

    async def run():

        collection = get_logs_collection()

        await collection.insert_one(
            {
                "event_type": event_type,
                "message": message,
            }
        )

    asyncio.run(run())