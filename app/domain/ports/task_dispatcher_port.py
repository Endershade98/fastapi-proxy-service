# app/domain/ports/task_dispatcher_port.py

from abc import ABC, abstractmethod
from typing import Any


class TaskDispatcherPort(ABC):

    @abstractmethod
    async def dispatch_cache_set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def dispatch_retry(
        self,
        resource: str
    ) -> str:
        raise NotImplementedError