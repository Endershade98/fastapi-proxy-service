# tests/unit/domain/value_objects/test_client_ip.py

import ipaddress

import pytest

from app.domain.exceptions import InvalidIPError
from app.domain.value_objects.client_ip import ClientIP


def test_creates_ipv4_address():
    client_ip = ClientIP("192.168.1.10")

    assert client_ip.value == "192.168.1.10"


def test_creates_ipv6_address():
    client_ip = ClientIP("2001:db8::1")

    assert client_ip.value == "2001:db8::1"


def test_normalizes_ipv4_address():
    client_ip = ClientIP("127.0.0.1")

    assert client_ip.value == str(ipaddress.ip_address("127.0.0.1"))


def test_normalizes_ipv6_address():
    client_ip = ClientIP("2001:0db8:0000:0000:0000:0000:0000:0001")

    assert client_ip.value == "2001:db8::1"


def test_rejects_invalid_ip():
    with pytest.raises(InvalidIPError):
        ClientIP("not-an-ip")


def test_rejects_empty_ip():
    with pytest.raises(InvalidIPError):
        ClientIP("")


def test_is_immutable():
    client_ip = ClientIP("127.0.0.1")

    with pytest.raises(AttributeError):
        client_ip.value = "10.0.0.1"


def test_string_representation():
    client_ip = ClientIP("127.0.0.1")

    assert str(client_ip) == "127.0.0.1"