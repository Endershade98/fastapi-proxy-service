# app/infrastructure/tasks/celery_task_reader.py

from celery.result import AsyncResult


class CeleryTaskReader:

    def __init__(self, celery_app):
        self.celery_app = celery_app

    def get_result(self, task_id: str):
        return AsyncResult(task_id, app=self.celery_app)