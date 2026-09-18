# app/infrastructure/celery/tasks/task_events.py

from app.infrastructure.celery.celery_app import celery_app
from app.infrastructure.db.mongodb import get_mongo
from datetime import datetime, timezone


async def _write(event: dict):
    mongo = get_mongo()
    await mongo.get_collection("task_events").insert_one(event)


@celery_app.task(name="task_event_received")
def task_received(task_id: str):
    import asyncio
    asyncio.run(_write({
        "task_id": task_id,
        "event": "RECEIVED",
        "ts": datetime.now(timezone.utc).isoformat()
    }))


@celery_app.task(name="task_event_started")
def task_started(task_id: str):
    import asyncio
    asyncio.run(_write({
        "task_id": task_id,
        "event": "STARTED",
        "ts": datetime.now(timezone.utc).isoformat()
    }))


@celery_app.task(name="task_event_succeeded")
def task_succeeded(task_id: str):
    import asyncio
    asyncio.run(_write({
        "task_id": task_id,
        "event": "SUCCEEDED",
        "ts": datetime.now(timezone.utc).isoformat()
    }))


@celery_app.task(name="task_event_failed")
def task_failed(task_id: str, error: str):
    import asyncio
    asyncio.run(_write({
        "task_id": task_id,
        "event": "FAILED",
        "error": error,
        "ts": datetime.now(timezone.utc).isoformat()
    }))