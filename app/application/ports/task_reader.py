# app/application/ports/task_reader.py

from abc import ABC, abstractmethod
from typing import Any


class TaskReaderPort(ABC):
    """
    Application port for reading asynchronous task state.
    """

    @abstractmethod
    def get_result(self, task_id: str) -> Any:
        raise NotImplementedError