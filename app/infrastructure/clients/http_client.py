# app/infrastructure/clients/http_client.py

import httpx
from app.domain.ports.remote_resource_port import RemoteResourcePort


class HttpClient(RemoteResourcePort):

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10)

    async def fetch(self, url: str):
        response = await self.client.get(url)
        response.raise_for_status()

        content_type = response.headers.get("content-type", "")

        # JSON API
        if "application/json" in content_type:
            return response.json()

        # HTML / text fallback (IMPORTANT per proxy e2e)
        return response.text