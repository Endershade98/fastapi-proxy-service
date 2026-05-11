# app/domain/ports/remote_resource_port.py

from abc import ABC, abstractmethod
from typing import Any


class RemoteResourcePort(ABC):

    @abstractmethod
    async def fetch(self, resource: str) -> Any:
        """
        Fetch data from an external resource.
        Domain does not care if HTTP, gRPC, MQ, etc.
        """
        raise NotImplementedError