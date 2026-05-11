# tests/unit/domain/test_exceptions.py

import pytest

from app.domain.exceptions import (
    InvalidIPError,
    InvalidQuotaError,
    InvalidTTLError,
    DomainException
)


def test_should_inherit_from_domain_exception():
    assert issubclass(InvalidIPError, DomainException)
    assert issubclass(InvalidQuotaError, DomainException)
    assert issubclass(InvalidTTLError, DomainException)


def test_should_have_message():
    err = InvalidIPError("wrong-ip")

    assert "wrong-ip" in str(err)