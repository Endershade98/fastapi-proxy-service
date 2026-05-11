# app/main.py

from fastapi import FastAPI
from typing import Optional

from app.bootstrap.dummies import DummyLogger, DummyRateLimiter
from app.interfaces.api.router import router
from app.interfaces.middleware.rate_limiter import RateLimiterMiddleware

from app.infrastructure.rate_limiter.redis_rate_limiter import RedisRateLimiter
from app.infrastructure.cache.redis_client import RedisClient
from app.infrastructure.logging.mongo_logger import MongoLogger
from app.infrastructure.db.mongodb import get_mongo




def create_app(testing: bool = False, rate_limiter=None, logger=None):
    app = FastAPI()

    if testing:
        # dependency injection finta per test
        rate_limiter = rate_limiter or DummyRateLimiter()
        logger = logger or DummyLogger()
    else:
        mongo = get_mongo()
        logger = MongoLogger()
        redis_client = RedisClient()
        rate_limiter = RedisRateLimiter(redis_client)

    app.add_middleware(
        RateLimiterMiddleware,
        rate_limiter=rate_limiter,
        logger=logger
    )

    app.include_router(router)

    return app