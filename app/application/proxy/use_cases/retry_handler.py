# app/application/proxy/use_cases/retry_handler.py

from app.domain.ports.task_dispatcher_port import TaskDispatcherPort


class RetryHandler:

    def __init__(self, dispatcher: TaskDispatcherPort):
        self._dispatcher = dispatcher

    async def execute(self, resource: str) -> str:
        return await self._dispatcher.dispatch_retry(resource)