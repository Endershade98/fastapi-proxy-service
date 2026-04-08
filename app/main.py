from fastapi import FastAPI
from app.interfaces.api.router import api_router
from app.interfaces.middleware.rate_limiter import RateLimiterMiddleware
from infrastructure.rate_limiter.redis_rate_limiter import RedisRateLimiter
from app.infrastructure.cache.redis_client import RedisClient

app = FastAPI()

# istanze concrete
redis_client = RedisClient()
rate_limiter_adapter = RedisRateLimiter(redis_client)

# aggiunta middleware
app.add_middleware(RateLimiterMiddleware, rate_limiter=rate_limiter_adapter)

# router principale
app.include_router(api_router)