import pytest
from app.infrastructure.cache.cache_service import RedisCacheService

@pytest.fixture
async def cache_service():
    cache = RedisCacheService()
    yield cache