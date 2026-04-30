# app/infrastructure/celery/celery_app.py
from celery import Celery
from app.config.settings import settings

celery_app = Celery(
    "proxy_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)