# tests/unit/domain/test_client_ip.py

import pytest
from app.domain.value_objects.client_ip import ClientIP
from app.domain.exceptions import InvalidIPError


def test_valid_ip_normalization():
    ip = ClientIP("127.0.0.1")
    assert ip.value == "127.0.0.1"


def test_invalid_ip_raises():
    with pytest.raises(InvalidIPError):
        ClientIP("not-an-ip")