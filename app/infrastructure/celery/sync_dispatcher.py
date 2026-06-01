# app/infrastructure/celery/sync_dispatcher.py

import uuid

from app.domain.ports.task_dispatcher_port import (
    TaskDispatcherPort
)


class SyncTaskDispatcher(TaskDispatcherPort):

    async def dispatch(
        self,
        task: str,
        payload: dict
    ) -> str:

        return str(uuid.uuid4())