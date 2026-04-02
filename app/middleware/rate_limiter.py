from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.cache.redis_client import redis_client

class RateLimiterMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        key = f"rate:{client_ip}"

        count = await redis_client.incr(key)

        if count == 1:
            await redis_client.expire(key, 60)

        if count > 10:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )

        return await call_next(request)