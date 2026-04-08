# app/interfaces/api/routes/proxy.py
from fastapi import APIRouter, HTTPException
from app.application.proxy.use_cases.cache_management import CacheManager
from app.infrastructure.cache.redis_client import RedisClient
from app.domain.value_objects.cache_entry import CacheEntry

router = APIRouter()

# istanza concreta della cache
redis_client = RedisClient()
cache_manager = CacheManager(cache_service=redis_client)  # usa RedisClient come servizio concreto

async def fetch_from_upstream(url: str) -> dict:
    """
    Funzione placeholder per simulare fetch da upstream.
    """
    # qui andrebbe la logica di forward request
    return {"url": url, "data": "upstream response"}

@router.post("/")
async def proxy_endpoint(payload: dict):
    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Missing 'url' in payload")

    cached = False
    # ottieni o genera cache entry
    entry: CacheEntry = await cache_manager.get_or_set(
        key=url,
        value_supplier=lambda: fetch_from_upstream(url),
        ttl=60
    )

    if not entry.is_expired:
        cached = True

    return {"data": entry.value, "cached": cached}