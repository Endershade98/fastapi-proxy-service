import httpx
import asyncio
from app.core.config import settings
from app.core.exceptions import (
    UpstreamServiceError,
    UpstreamTimeoutError
)
from app.core.config import settings

async def fetch(url: str):
    last_exception = None

    for attempt in range(1, settings.MAX_RETRIES + 1):
        try:
            async with httpx.AsyncClient(timeout=settings.TIMEOUT) as client:
                response = await client.get(url)

                # Gestione errori 5xx
                if response.status_code >= 500:
                    raise UpstreamServiceError(
                        status_code=response.status_code,
                        message="Upstream server error"
                    )

                return response

        except (httpx.TimeoutException, httpx.RequestError, UpstreamServiceError) as e:
            last_exception = e
            wait_time = settings.BACKOFF_FACTOR * (2 ** (attempt - 1))
            print(f"[Retry {attempt}/{settings.MAX_RETRIES}] waiting {wait_time}s due to {e}")
            await asyncio.sleep(wait_time)

    # Dopo tutti i retry falliti
    if isinstance(last_exception, httpx.TimeoutException):
        raise UpstreamTimeoutError()
    elif isinstance(last_exception, UpstreamServiceError):
        raise last_exception
    else:
        raise UpstreamServiceError(status_code=502, message=str(last_exception))