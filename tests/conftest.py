import pytest
from httpx import AsyncClient, ASGITransport

from app.main import create_app
from app.core.dependencies import get_cache_manager


class FakeCacheManager:
    async def get_or_set(self, key, value_supplier, ttl):
        class Entry:
            value = {"mock": True}
            is_expired = True  # MISS → cached = False
        return Entry()


@pytest.fixture
def app_instance():
    app = create_app(testing=True)

    app.dependency_overrides[get_cache_manager] = lambda: FakeCacheManager()

    return app


@pytest.fixture
async def client(app_instance):
    transport = ASGITransport(app=app_instance)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as c:
        yield c