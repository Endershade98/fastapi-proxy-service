# tests/e2e/test_proxy_flow.py
import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from fastapi import FastAPI
from app.interfaces.api.router import api_router
from app.interfaces.middleware.rate_limiter import RateLimiterMiddleware

# Dummy rate limiter per bypassare Redis
class DummyRateLimiter:
    async def allow(self, request):
        return True  # sempre consentito

# Creiamo una copia dell'app solo per i test
def create_test_app():
    app = FastAPI()
    app.add_middleware(RateLimiterMiddleware, rate_limiter=DummyRateLimiter())
    app.include_router(api_router)
    return app

@pytest.mark.asyncio
async def test_proxy_cache_flow():
    test_app = create_test_app()
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        url = "http://example.com/api"

        # prima richiesta → cache miss
        response1 = await client.post("/proxy/", json={"url": url})
        assert response1.status_code == 200

        # seconda richiesta → cache hit
        response2 = await client.post("/proxy/", json={"url": url})
        assert response2.status_code == 200