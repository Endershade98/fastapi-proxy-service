# app/main.py

from fastapi import FastAPI

from app.interfaces.api.router import api_router
from app.interfaces.middleware.rate_limiter import RateLimiterMiddleware

from app.infrastructure.rate_limiter.redis_rate_limiter import RedisRateLimiter
from app.infrastructure.cache.redis_client import redis_client
from app.infrastructure.logging.mongo_logger import MongoLogger
from app.infrastructure.db.mongodb import get_mongo


def create_app(testing: bool = False):

    app = FastAPI()

    if testing:
        # fake infra injected via conftest
        rate_limiter = None
        logger = None
    else:
        mongo = get_mongo()
        logger = MongoLogger(collection=mongo.get_collection("logs"))
        rate_limiter = RedisRateLimiter(redis_client)

    app.add_middleware(
        RateLimiterMiddleware,
        rate_limiter=rate_limiter,
        logger=logger
    )

    app.include_router(api_router)

    return app


app = create_app()