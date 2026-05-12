# app/interfaces/middleware/rate_limiter.py

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from typing import Callable

from app.domain.ports.rate_limiter_port import RateLimiterPort
from app.domain.ports.logger_port import LoggerPort


class RateLimiterMiddleware(BaseHTTPMiddleware):

    def __init__(
        self,
        app,
        rate_limiter: RateLimiterPort,
        logger: LoggerPort
    ):
        super().__init__(app)
        self.rate_limiter = rate_limiter
        self.logger = logger

    async def dispatch(self, request: Request, call_next: Callable):

        ip = request.client.host if request.client else "unknown"

        allowed = await self.rate_limiter.is_allowed(ip)

        if not allowed:
            return self._rate_limited_response()

        response = await call_next(request)

        await self.logger.log_event(
            event_type="http_request",
            data={
                "ip": ip,
                "path": request.url.path
            }
        )

        return response