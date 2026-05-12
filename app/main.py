# app/main.py

from fastapi import FastAPI

from app.bootstrap.dummies import DummyLogger, DummyRateLimiter
from app.interfaces.api.router import router
from app.interfaces.middleware.rate_limiter import RateLimiterMiddleware

from app.infrastructure.rate_limiter.redis_rate_limiter import RedisRateLimiter
from app.infrastructure.cache.redis_client import RedisClient
from app.infrastructure.app_logging.mongo_logger import MongoLogger
from app.infrastructure.db.mongodb import get_mongo


def create_app(testing: bool = False, rate_limiter=None, logger=None):
    app = FastAPI()

    # ----------------------------
    # Dependency resolution
    # ----------------------------
    if testing:
        rate_limiter = rate_limiter or DummyRateLimiter()
        logger = logger or DummyLogger()

    else:
        # Infra wiring (production)
        mongo_client = get_mongo()
        redis_client = RedisClient()

        rate_limiter = RedisRateLimiter(redis_client)
        logger = MongoLogger(mongo_client)

    # ----------------------------
    # Middleware
    # ----------------------------
    app.add_middleware(
        RateLimiterMiddleware,
        rate_limiter=rate_limiter,
        logger=logger,
    )

    # ----------------------------
    # Routes
    # ----------------------------
    app.include_router(router)

    return app