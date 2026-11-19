# app/infrastructure/clients/http_client.py

import httpx

from app.application.ports.remote_resource import (
    RemoteResourcePort,
)


class HttpClient(RemoteResourcePort):

    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
    ):
        self._client = client or httpx.AsyncClient(
            timeout=3
        )

    async def fetch(self, url: str):
        response = await self._client.get(url)

        response.raise_for_status()

        content_type = response.headers.get(
            "content-type",
            "",
        )

        if "application/json" in content_type:
            return response.json()

        return response.text

    async def close(self) -> None:
        await self._client.aclose()