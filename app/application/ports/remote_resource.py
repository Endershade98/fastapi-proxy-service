# app/application/ports/remote_resource.py

from abc import ABC, abstractmethod
from typing import Any


class RemoteResourcePort(ABC):
    """
    Application port for retrieving resources from remote systems.

    HTTP, external APIs and other protocols are infrastructure concerns.
    """

    @abstractmethod
    async def fetch(self, resource: str) -> Any:
        raise NotImplementedError