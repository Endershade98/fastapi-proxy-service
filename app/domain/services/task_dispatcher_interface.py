# app/domain/services/task_dispatcher_interface.py

from abc import ABC, abstractmethod
from typing import Any


class TaskDispatcherInterface(ABC):

    @abstractmethod
    async def dispatch_cache_set(
        self,
        key: str,
        value: Any,
        ttl: int
    ) -> None:
        pass

    @abstractmethod
    async def dispatch_retry(
        self,
        url: str
    ) -> str:
        pass