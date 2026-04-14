# app/interfaces/middleware/rate_limiter.py
from fastapi import Request
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from app.domain.value_objects.client_ip import ClientIP
from app.domain.services.rate_limit_policy import RateLimitPolicy
from app.domain.events.log_event import LogEvent


class RateLimiterMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, rate_limiter, logger, window: int = 60):
        super().__init__(app)
        self.rate_limiter = rate_limiter
        self.logger = logger
        self.policy = RateLimitPolicy(limit=10, period=window)
        self.window = window

    async def dispatch(self, request: Request, call_next: Callable):

        client_ip = ClientIP(request.client.host)
        key = f"rate:{client_ip.value}"

        try:
            count = await self.rate_limiter.increment(key, self.window)

            if not self.policy.is_allowed(count):

                await self._safe_log(LogEvent(
                    event_type="RATE_LIMIT_EXCEEDED",
                    message="Rate limit exceeded",
                    client_ip=client_ip.value,
                    metadata={"count": count}
                ))

                return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

            return await call_next(request)

        except Exception as e:

            await self._safe_log(LogEvent(
                event_type="RATE_LIMIT_ERROR",
                message=str(e),
                client_ip=client_ip.value
            ))

            return await call_next(request)

    async def _safe_log(self, event):
        try:
            await self.logger.log(event)
        except Exception:
            pass