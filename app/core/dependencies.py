from app.infrastructure.cache.redis_client import redis_client

def get_redis_client():
    return redis_client