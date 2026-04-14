# app/infrastructure/clients/http_client.py
import httpx


class HttpClient:

    def __init__(self):
        self.client = httpx.AsyncClient()

    async def request(self, method: str, url: str, **kwargs):
        return await self.client.request(method, url, **kwargs)

    async def fetch(self, url: str) -> dict:
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()