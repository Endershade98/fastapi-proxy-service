# app/infrastructure/celery/dispatcher.py

from app.application.ports.task_dispatcher import (
    TaskDispatcherPort,
)


class CeleryTaskDispatcher(TaskDispatcherPort):

    def __init__(self, task_router):
        self._task_router = task_router

    async def dispatch(
        self,
        task: str,
        payload: dict,
    ) -> str:

        result = self._task_router.delay(
            task,
            payload,
        )

        return result.id