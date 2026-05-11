# tests/unit/domain/test_client_ip.py

import pytest

from app.domain.value_objects.client_ip import ClientIP
from app.domain.exceptions import InvalidIPError


def test_should_create_valid_ipv4():
    ip = ClientIP("192.168.1.10")

    assert ip.value == "192.168.1.10"


def test_should_create_valid_ipv6():
    ip = ClientIP("2001:db8::1")

    assert ip.value == "2001:db8::1"


def test_should_raise_when_invalid_ip():
    with pytest.raises(InvalidIPError):
        ClientIP("not-an-ip")


def test_should_be_equal_when_same_value():
    a = ClientIP("127.0.0.1")
    b = ClientIP("127.0.0.1")

    assert a == b