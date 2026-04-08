import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

# Event loop per async tests
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# FastAPI client
@pytest.fixture
def client():
    return TestClient(app)