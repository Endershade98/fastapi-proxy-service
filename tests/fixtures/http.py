import pytest

@pytest.fixture
def mock_http_response():
    class MockResponse:
        status_code = 200

        def json(self):
            return {"mock": True}

        @property
        def text(self):
            return "mock text"

    return MockResponse()