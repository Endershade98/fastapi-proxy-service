# app/infrastructure/celery/dispatcher.py

from app.domain.ports.task_dispatcher_port import TaskDispatcherPort


class CeleryTaskDispatcher(TaskDispatcherPort):

    def __init__(self, task_router):
        self.task_router = task_router

    async def dispatch(self, task: str, payload: dict) -> str:
        result = self.task_router.delay(task, payload)
        return result.id