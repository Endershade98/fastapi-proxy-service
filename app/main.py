# app/main.py

from fastapi import FastAPI

from app.bootstrap.container import (
    get_rate_limit_use_case,
    get_event_publisher,
)

from app.interfaces.api.router import router
from app.interfaces.middleware.rate_limiter import RateLimiterMiddleware
from app.bootstrap.dummies import DummyEventPublisher


def create_app(testing: bool = False):

    app = FastAPI()

    # =====================================================
    # DEPENDENCIES
    # =====================================================

    rate_limit_use_case = get_rate_limit_use_case()

    if testing:
        publisher = DummyEventPublisher()
    else:
        publisher = get_event_publisher()

    # =====================================================
    # MIDDLEWARE
    # =====================================================
    app.add_middleware(
        RateLimiterMiddleware,
        rate_limit_use_case=rate_limit_use_case,
        publisher=publisher,
    )

    # =====================================================
    # ROUTES
    # =====================================================
    app.include_router(router)

    return app