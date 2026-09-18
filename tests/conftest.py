# tests/conftest.py

import pytest
from app.main import create_app


@pytest.fixture
def app():
    return create_app(testing=True)


@pytest.fixture
def client(app):
    from fastapi.testclient import TestClient
    return TestClient(app)