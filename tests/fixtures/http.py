# tests/fixtures/http.py

import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def http_client_mock():
    mock = AsyncMock()

    mock.request.return_value.json.return_value = {"ok": True}
    mock.request.return_value.status_code = 200

    return mock