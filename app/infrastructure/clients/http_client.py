# app/infrastructure/clients/http_client.py
import httpx


class HttpClient:

    def __init__(self):
        self.client = httpx.AsyncClient()

    async def request(self, method: str, url: str, **kwargs):
        return await self.client.request(method, url, **kwargs)