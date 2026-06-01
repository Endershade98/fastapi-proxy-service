# app/bootstrap/container.py

from functools import lru_cache

from app.config.settings import settings

# Use Cases
from app.application.caching.use_cases.get_or_set_cache import GetOrSetCacheUseCase
from app.application.proxy.use_cases.forward_proxy_request import ForwardProxyRequestUseCase
from app.application.security.use_cases.enforce_rate_limit import EnforceRateLimitUseCase
from app.application.tasks.use_cases.get_task_status import GetTaskStatusUseCase

# Domain
from app.domain.policies.rate_limit_policy import RateLimitPolicy
from app.domain.value_objects.request_quota import RequestQuota

# Infrastructure
from app.infrastructure.cache.redis_client import RedisClient
from app.infrastructure.clients.http_client import HttpClient
from app.infrastructure.rate_limiter.redis_rate_limiter import RedisRateLimiter
from app.infrastructure.celery.sync_dispatcher import SyncTaskDispatcher
from app.infrastructure.celery.celery_app import celery_app
from app.infrastructure.tasks.celery_task_reader import CeleryTaskReader
from app.infrastructure.cache.cache_service import CacheService

from app.infrastructure.app_logging.mongo_event_publisher import MongoEventPublisher


@lru_cache
def get_cache_service():
    return CacheService(RedisClient())


@lru_cache
def get_http_client():
    return HttpClient()


@lru_cache
def get_rate_limiter_repository():
    return RedisRateLimiter(
        redis_client=RedisClient()
    )


@lru_cache
def get_rate_limit_policy():
    return RateLimitPolicy(
        RequestQuota(
            limit=settings.RATE_LIMIT_REQUESTS,
            window_seconds=settings.RATE_LIMIT_WINDOW,
        )
    )


@lru_cache
def get_task_reader():
    return CeleryTaskReader(celery_app)


# =========================
# USE CASES
# =========================

def get_cache_use_case():
    return GetOrSetCacheUseCase(
        cache=get_cache_service(),
    )


def get_forward_proxy_use_case():
    return ForwardProxyRequestUseCase(
        remote_resource=get_http_client(),
        cache_use_case=get_cache_use_case(),
    )


def get_rate_limit_use_case():
    return EnforceRateLimitUseCase(
        repository=get_rate_limiter_repository(),
        policy=get_rate_limit_policy(),
    )


def get_task_status_use_case():
    return GetTaskStatusUseCase(
        task_reader=get_task_reader(),
    )


@lru_cache
def get_event_publisher():
    return MongoEventPublisher()