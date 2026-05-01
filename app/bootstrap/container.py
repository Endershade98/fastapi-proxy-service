# app/bootstrap/container.py

from app.application.proxy.use_cases.forward_request import ForwardRequestUseCase
from app.infrastructure.cache.redis_client import RedisClient
from app.application.proxy.use_cases.cache_management import CacheManager



# DEFAULT PROD DEPENDENCY
def get_cache_manager():
    redis_client = RedisClient()
    return CacheManager(cache_service=redis_client)


def get_http_client():
    from app.infrastructure.clients.http_client import HttpClient
    return HttpClient()


def get_forward_request_use_case():
    cache_manager = get_cache_manager()
    http_client = get_http_client()
    return ForwardRequestUseCase(cache_manager=cache_manager, http_client=http_client)