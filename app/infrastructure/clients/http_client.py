# app/infrastructure/clients/http_client.py

import httpx
from app.domain.services.http_client_interface import HttpClientInterface


class HttpClient(HttpClientInterface):

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10)

    async def fetch(self, url: str) -> dict:
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def request(self, method: str, url: str, **kwargs):
        response = await self.client.request(method, url, **kwargs)
        response.raise_for_status()
        return response