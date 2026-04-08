# app/interfaces/middleware/rate_limiter.py
from starlette.middleware.base import BaseHTTPMiddleware
from app.domain.services.rate_limiter_interface import RateLimiterInterface

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limiter: RateLimiterInterface):
        super().__init__(app)
        self.rate_limiter = rate_limiter

    async def dispatch(self, request, call_next):
        if not await self.rate_limiter.allow(request):
            from starlette.responses import JSONResponse
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
        return await call_next(request)