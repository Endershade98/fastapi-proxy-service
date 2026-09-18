# app/infrastructure/celery/tasks/log_tasks.py

import asyncio
from datetime import datetime, timezone

from app.infrastructure.celery.celery_app import celery_app
from app.infrastructure.db.mongodb import get_mongo


@celery_app.task(name="log_event_task")
def log_event_task(payload: dict):

    async def run():
        mongo = get_mongo()

        collection = mongo.get_collection("system_events")

        await collection.insert_one({
            "payload": payload,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })

    asyncio.run(run())