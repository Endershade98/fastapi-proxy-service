# app/interfaces/middleware/rate_limiter.py

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from typing import Callable

from app.application.security.use_cases.enforce_rate_limit import EnforceRateLimitUseCase
from app.domain.ports.event_publisher_port import EventPublisherPort

from app.domain.events.system_events import (
    RequestLoggedEvent,
    RateLimitExceededEvent,
)

from app.domain.value_objects.client_ip import ClientIP


class RateLimiterMiddleware(BaseHTTPMiddleware):

    def __init__(
        self,
        app,
        rate_limit_use_case: EnforceRateLimitUseCase,
        publisher: EventPublisherPort,
    ):
        super().__init__(app)
        self.rate_limit_use_case = rate_limit_use_case
        self.publisher = publisher

    async def dispatch(self, request: Request, call_next: Callable):

        # =====================================================
        # CLIENT IP (REAL VALUE OBJECT USAGE)
        # =====================================================
        raw_ip = (
            request.headers.get("x-forwarded-for")
            or (request.client.host if request.client else None)
            or "127.0.0.1"
        )

        ip_obj = ClientIP(raw_ip.split(",")[0].strip())
        ip = str(ip_obj)

        # =====================================================
        # RATE LIMIT CHECK
        # =====================================================
        result = await self.rate_limit_use_case.execute(ip)

        if not result.allowed:

            await self.publisher.publish(
                RateLimitExceededEvent(
                    client_ip=ip,
                    limit=result.limit,
                    window_seconds=self.rate_limit_use_case.policy.window_seconds,
                )
            )

            return self._rate_limited_response(
                limit=result.limit,
                remaining=result.remaining,
                retry_after=result.retry_after_seconds,
            )

        # =====================================================
        # PROCESS REQUEST
        # =====================================================
        response = await call_next(request)

        # =====================================================
        # ADD RATE LIMIT HEADERS (EPIC 2 FIX)
        # =====================================================
        response.headers["X-RateLimit-Limit"] = str(result.limit)
        response.headers["X-RateLimit-Remaining"] = str(result.remaining)
        response.headers["Retry-After"] = str(result.retry_after_seconds)

        # =====================================================
        # LOG REQUEST EVENT
        # =====================================================
        await self.publisher.publish(
            RequestLoggedEvent(
                event_type="http_request",
                path=str(request.url.path),
                client_ip=ip,
            )
        )

        return response

    def _rate_limited_response(self, limit: int, remaining: int, retry_after: int):

        from fastapi.responses import JSONResponse

        return JSONResponse(
            status_code=429,
            headers={
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": "0",
                "Retry-After": str(retry_after),
            },
            content={
                "detail": "Too many requests",
                "limit": limit,
                "remaining": remaining,
                "retry_after": retry_after,
            },
        )