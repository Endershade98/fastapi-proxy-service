from app.clients.http_client import fetch
from app.cache.cache_service import CacheService

cache = CacheService()

class ProxyService:

    async def forward_request(self, url: str):
        cache_key = f"proxy:{url}"

        cached = await cache.get(cache_key)
        if cached:
            return cached

        response = await fetch(url)

        result = {
            "status_code": response.status_code,
            "data": response.json()
        }

        await cache.set(cache_key, result)

        return result