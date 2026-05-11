# app/infrastructure/celery/tasks/proxy_tasks.py

import asyncio
from app.infrastructure.celery.celery_app import celery_app
from app.infrastructure.clients.http_client import HttpClient


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
    name="retry_proxy_request"
)
def retry_proxy_request(self, url):

    async def run():
        client = HttpClient()
        data = await client.fetch(url)
        return data

    return asyncio.run(run())