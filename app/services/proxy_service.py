import logging
from typing import Any

from app.clients.http_client import fetch
from app.core.exceptions import (
    UpstreamServiceError,
    UpstreamTimeoutError,
)
from app.cache.cache_service import CacheService

logger = logging.getLogger(__name__)
cache = CacheService()


class ProxyService:
    """
    Service per il proxy HTTP.
    - Usa cache Redis
    - Gestisce errori upstream
    - Supporta sia JSON che raw text
    """

    async def forward_request(self, url: str, force_json: bool = False) -> dict[str, Any]:
        """
        Inoltra la richiesta al server esterno.
        
        Args:
            url (str): URL di destinazione
            force_json (bool): se True forza risposta JSON, altrimenti fallback su testo

        Returns:
            dict: result con status_code e data/error
        """
        url = str(url)
        cache_key = f"proxy:{url}"

        # Controllo cache
        cached = await cache.get(cache_key)
        if cached:
            logger.info(f"[Cache HIT] {url}")
            return cached
        else:
            logger.info(f"[Cache MISS] {url}")

        try:
            response = await fetch(url)
            result: dict[str, Any] = {"status_code": response.status_code}

            # Parsing sicuro
            if force_json:
                # Se vogliamo solo JSON, errore se non JSON
                try:
                    result["data"] = response.json()
                except Exception:
                    logger.error(f"[ProxyService] Invalid JSON response from {url}")
                    result["error"] = "Invalid JSON response"
                    result["status_code"] = 502
            else:
                # Fallback: prova JSON, altrimenti testo
                try:
                    result["data"] = response.json()
                except Exception:
                    result["data"] = response.text

            # Salvo in cache
            await cache.set(cache_key, result)
            return result

        except UpstreamTimeoutError:
            logger.error(f"[ProxyService] Timeout for {url}")
            return {
                "status_code": 504,
                "error": "Upstream timeout"
            }

        except UpstreamServiceError as e:
            logger.error(f"[ProxyService] Upstream error {e.status_code} for {url}: {e.message}")
            return {
                "status_code": e.status_code,
                "error": e.message
            }

        except Exception as e:
            logger.exception(f"[ProxyService] Unexpected error for {url}: {e}")
            return {
                "status_code": 500,
                "error": "Internal proxy error"
            }