# app/infrastructure/tasks/celery_task_reader.py

from celery.result import AsyncResult

from app.application.ports.task_reader import TaskReaderPort


class CeleryTaskReader(TaskReaderPort):

    def __init__(self, celery_app):
        self._celery_app = celery_app

    def get_result(self, task_id: str):
        return AsyncResult(
            task_id,
            app=self._celery_app,
        )