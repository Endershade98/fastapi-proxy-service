from app.clients.http_client import fetch
from app.cache.cache_service import CacheService
import httpx

cache = CacheService()

class ProxyService:

    async def forward_request(self, url: str):
        url = str(url)  # ✅ safety

        cache_key = f"proxy:{url}"

        # 🔹 CACHE
        cached = await cache.get(cache_key)
        if cached:
            return cached

        try:
            response = await fetch(url)

            try:
                data = response.json()
            except Exception:
                data = response.text

            result = {
                "status_code": response.status_code,
                "data": data
            }

            await cache.set(cache_key, result)

            return result

        except httpx.RequestError as e:
            return {
                "status_code": 500,
                "error": f"Request failed: {str(e)}"
            }