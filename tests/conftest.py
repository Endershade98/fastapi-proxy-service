# tests/conftest.py

import pytest


@pytest.fixture
def app():
    from app.main import create_app

    return create_app(testing=True)


@pytest.fixture
def client(app):
    from fastapi.testclient import TestClient

    return TestClient(app)