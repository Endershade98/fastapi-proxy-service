# app/interfaces/middleware/rate_limiter.py

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from typing import Callable

from app.domain.ports.rate_limiter_port import RateLimiterPort
from app.domain.ports.event_publisher_port import EventPublisherPort
from app.domain.events.system_events import (
    RequestLoggedEvent,
    RateLimitExceededEvent,
)

from app.application.security.use_cases.enforce_rate_limit import EnforceRateLimitUseCase


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

        ip = request.headers.get(
            "x-forwarded-for",
            request.client.host if request.client else "unknown",
        )

        # ==========================
        # DOMAIN RATE LIMIT DECISION
        # ==========================
        result = await self.rate_limit_use_case.execute(ip)

        if not result.allowed:
            await self.publisher.publish(
                RateLimitExceededEvent(
                    client_ip=ip,
                    limit=result.limit,
                    window_seconds=self.rate_limit_use_case.policy.window_seconds,
                )
            )

            return self._rate_limited_response()

        # ==========================
        # REQUEST FLOW
        # ==========================
        response = await call_next(request)

        await self.publisher.publish(
            RequestLoggedEvent(
                event_type="http_request",
                path=request.url.path,
                client_ip=ip,
            )
        )

        return response

    def _rate_limited_response(self):
        from fastapi.responses import JSONResponse

        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"},
        )