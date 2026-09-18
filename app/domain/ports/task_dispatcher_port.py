# app/domain/ports/task_dispatcher_port.py

from abc import ABC, abstractmethod
from typing import Any


class TaskDispatcherPort(ABC):

    @abstractmethod
    async def dispatch(self, task: str, payload: dict) -> str:
        raise NotImplementedError