# app/interfaces/middleware/rate_limiter.py

from typing import Callable

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.application.security.use_cases.enforce_rate_limit import (
    EnforceRateLimitUseCase,
)


class RateLimiterMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, rate_limiter=None, logger=None, window: int = 60):
        super().__init__(app)

        self.rate_limiter = rate_limiter
        self.logger = logger
        self.window = window

    async def dispatch(self, request: Request, call_next: Callable):

        ip = request.client.host if request.client else "unknown"

        result = await self.use_case.execute(ip)

        if not result.allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "limit": result.limit,
                    "remaining": result.remaining,
                },
            )

        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(result.limit)
        response.headers["X-RateLimit-Remaining"] = str(result.remaining)

        return response