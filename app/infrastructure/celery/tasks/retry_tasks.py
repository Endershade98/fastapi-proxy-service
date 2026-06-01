# app/infrastructure/celery/tasks/retry_tasks.py

from app.infrastructure.celery.celery_app import celery_app
from app.infrastructure.clients.http_client import HttpClient


@celery_app.task(name="retry_proxy_request")
def retry_proxy_request_task(url: str):

    import asyncio

    async def run():
        client = HttpClient()
        return await client.fetch(url)

    return asyncio.run(run())