# app/interfaces/middleware/rate_limiter.py
from fastapi import Request, Callable
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from app.domain.value_objects.client_ip import ClientIP
from app.domain.services.rate_limit_policy import RateLimitPolicy
from app.domain.events.log_event import LogEvent


class RateLimiterMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, rate_limiter, logger):
        super().__init__(app)
        self.rate_limiter = rate_limiter
        self.policy = RateLimitPolicy(limit=10)
        self.logger = logger
        self.window = 60
    
    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        """
        Middleware method to handle rate limiting for incoming requests.

        Args:
            request (Request): The incoming request object.
            call_next (Callable): The next middleware or route handler to call.
        
        Returns:
            Response: The response object.
        """
        client_ip = ClientIP(request.client.host)
        key = f"rate:{client_ip.value}"

        try:
            count = await self.rate_limiter.increment(key, self.window)

            # RATE LIMIT EXCEEDED
            if not self.policy.is_allowed(count):

                # LOG EVENT (best effort, non blocking)
                await self._safe_log(
                    LogEvent(
                        event_type="RATE_LIMIT_EXCEEDED",
                        message="Rate limit exceeded",
                        client_ip=client_ip.value,
                        metadata={"count": count, "window": self.window}
                    )
                )

                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded"}
                )

            return await call_next(request)

        except Exception as e:

            # fallback safety log
            await self._safe_log(
                LogEvent(
                    event_type="RATE_LIMIT_ERROR",
                    message=str(e),
                    client_ip=client_ip.value
                )
            )

            # fail-open strategy (NON bloccare traffico)
            return await call_next(request)
    
    async def _safe_log(self, event: LogEvent) -> None:
        """
        Log an event safely without blocking the request flow.
        Args:
            event (LogEvent): The event to be logged
        """
        try:
            await self.logger.log(event)
        except Exception:
            # NEVER block request flow because of logging failure
            pass