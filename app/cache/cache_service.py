# app/cache/cache_service.py
import json
from typing import Optional, Any
from app.infrastructure.cache.redis_client import redis_client
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class CacheService:
    """
    Infrastructure Layer: gestione della cache con hit/miss,
    TTL configurabile e serializzazione sicura.
    """

    async def get(self, key: str) -> Optional[Any]:
        """
        Recupera un valore dalla cache.
        Logga HIT o MISS.
        """
        try:
            value = await redis_client.get(key)
            if value:
                logger.info(f"[Cache HIT] key={key}")
                return json.loads(value)
            logger.info(f"[Cache MISS] key={key}")
            return None
        except Exception as e:
            logger.error(f"[Cache ERROR] Failed to get key={key}: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int = 60):
        """
        Inserisce un valore nella cache con TTL.
        """
        try:
            await redis_client.set(key, json.dumps(value), ex=ttl)
            logger.info(f"[Cache SET] key={key}, ttl={ttl}s")
        except Exception as e:
            logger.error(f"[Cache ERROR] Failed to set key={key}: {e}")