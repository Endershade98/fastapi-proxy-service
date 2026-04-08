# app/infrastructure/cache/cache_service.py
import json
import logging
from typing import Optional, Any
from app.infrastructure.cache.redis_client import redis_client  # istanza già creata

class CacheService:
    """
    Infrastructure Layer: gestione della cache con hit/miss,
    TTL configurabile e serializzazione sicura.
    """

    def __init__(self, client=None):
        self.client = client or redis_client

    async def get(self, key: str) -> Optional[Any]:
        try:
            value = await self.client.get(key)
            if value:
                logging.info(f"[Cache HIT] key={key}")
                return json.loads(value)
            logging.info(f"[Cache MISS] key={key}")
            return None
        except Exception as e:
            logging.error(f"[Cache ERROR] Failed to get key={key}: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int = 60):
        try:
            await self.client.set(key, json.dumps(value), ex=ttl)
            logging.info(f"[Cache SET] key={key}, ttl={ttl}s")
        except Exception as e:
            logging.error(f"[Cache ERROR] Failed to set key={key}: {e}")