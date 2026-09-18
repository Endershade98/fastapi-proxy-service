# app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.bootstrap.container import get_rate_limit_use_case, get_event_publisher
from app.interfaces.middleware.rate_limiter import RateLimiterMiddleware
from app.interfaces.api.router import router
from app.bootstrap.dummies import DummyEventPublisher
from app.infrastructure.cache.redis_client import RedisClient


def create_app(testing: bool = False):

    redis_client = RedisClient()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        # CLEAN SHUTDOWN
        try:
            await redis_client.close()
        except Exception:
            pass

    app = FastAPI(lifespan=lifespan)

    rate_limit_use_case = get_rate_limit_use_case()

    publisher = DummyEventPublisher() if testing else get_event_publisher()

    app.add_middleware(
        RateLimiterMiddleware,
        rate_limit_use_case=rate_limit_use_case,
        publisher=publisher,
    )

    app.include_router(router)

    return app