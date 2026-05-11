# app/application/proxy/use_cases/retry_handler.py

from app.domain.services.task_dispatcher_interface import TaskDispatcherInterface


class RetryHandler:

    def __init__(self, dispatcher: TaskDispatcherInterface):
        self.dispatcher = dispatcher

    async def dispatch_retry(self, url: str):
        return await self.dispatcher.dispatch_retry(url)