# app/domain/services/http_client_interface.py

from abc import ABC, abstractmethod
from typing import Any


class HttpClientInterface(ABC):

    @abstractmethod
    async def fetch(self, url: str) -> Any:
        pass