# app/bootstrap/container.py

from functools import lru_cache

from app.config.settings import settings

# Application
from app.application.proxy.use_cases.cache_management import GetOrSetCacheUseCase
from app.application.proxy.use_cases.forward_request import ForwardRequestUseCase
from app.application.proxy.use_cases.retry_handler import RetryHandler
from app.application.security.use_cases.enforce_rate_limit import (
    EnforceRateLimitUseCase,
)

# Domain
from app.domain.services.rate_limit_policy import RateLimitPolicy
from app.domain.value_objects.request_quota import RequestQuota

# Infrastructure
from app.infrastructure.cache.redis_client import RedisClient
from app.infrastructure.clients.http_client import HttpClient
from app.infrastructure.celery.sync_dispatcher import SyncTaskDispatcher
from app.infrastructure.celery.celery_dispatcher import CeleryTaskDispatcher
from app.infrastructure.rate_limiter.redis_rate_limiter import RedisRateLimiter


@lru_cache
def get_cache_service():
    return RedisClient()


@lru_cache
def get_http_client():
    return HttpClient()


@lru_cache
def get_rate_limiter_repository():
    return RedisRateLimiter(get_cache_service())


@lru_cache
def get_task_dispatcher():
    if settings.USE_CELERY:
        return CeleryTaskDispatcher()
    return SyncTaskDispatcher(get_cache_service())


@lru_cache
def get_rate_limit_policy():
    return RateLimitPolicy(
        RequestQuota(
            limit=settings.RATE_LIMIT_REQUESTS,
            period=settings.RATE_LIMIT_WINDOW,
        )
    )


def get_cache_manager():
    return GetOrSetCacheUseCase(
        cache_service=get_cache_service(),
        dispatcher=get_task_dispatcher(),
    )


def get_forward_request_use_case():
    return ForwardRequestUseCase(
        cache_manager=get_cache_manager(),
        http_client=get_http_client(),
    )


def get_retry_handler():
    return RetryHandler(
        dispatcher=get_task_dispatcher()
    )


def get_rate_limit_use_case():
    return EnforceRateLimitUseCase(
        repository=get_rate_limiter_repository(),
        policy=get_rate_limit_policy(),
    )

from app.infrastructure.tasks.celery_task_reader import CeleryTaskReader
from app.application.tasks.use_cases.get_task_status import GetTaskStatusUseCase
from app.infrastructure.celery.celery_app import celery_app


def get_task_status_use_case():
    return GetTaskStatusUseCase(
        task_reader=CeleryTaskReader(celery_app)
    )