from fastapi import FastAPI
from app.interfaces.api.router import api_router
from app.interfaces.middleware.rate_limiter import RateLimiterMiddleware
from app.infrastructure.rate_limiter.redis_rate_limiter import RedisRateLimiter
from app.infrastructure.cache.redis_client import redis_client
from app.infrastructure.logging.mongo_logger import MongoLogger

# APP INSTANCE
app = FastAPI()

# SINGLETON redis
rate_limiter = RedisRateLimiter(redis_client)

# SINGLETON logger
logger = MongoLogger()

# MIDDLEWARE rate limiter
app.add_middleware(
    RateLimiterMiddleware,
    rate_limiter=rate_limiter,
    logger=logger
)

# ROUTES 
app.include_router(api_router)