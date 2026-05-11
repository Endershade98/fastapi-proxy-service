# app/infrastructure/celery/celery_dispatcher.py

from app.infrastructure.celery.tasks.cache_tasks import save_cache_task

class CeleryTaskDispatcher:

    async def dispatch_cache_set(self, key, value, ttl):
        save_cache_task.delay(key, value, ttl)