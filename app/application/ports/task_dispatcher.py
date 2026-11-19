# app/application/ports/task_dispatcher.py

from abc import ABC, abstractmethod


class TaskDispatcherPort(ABC):
    """
    Application port for asynchronous task dispatching.
    """

    @abstractmethod
    async def dispatch(
        self,
        task: str,
        payload: dict,
    ) -> str:
        raise NotImplementedError