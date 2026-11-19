# tests/unit/domain/value_objects/test_request_quota.py

import pytest

from app.domain.exceptions import InvalidQuotaError
from app.domain.value_objects.request_quota import RequestQuota


def test_creates_valid_quota():
    quota = RequestQuota(
        limit=100,
        window_seconds=60,
    )

    assert quota.limit == 100
    assert quota.window_seconds == 60


def test_rejects_zero_limit():
    with pytest.raises(InvalidQuotaError):
        RequestQuota(
            limit=0,
            window_seconds=60,
        )


def test_rejects_negative_limit():
    with pytest.raises(InvalidQuotaError):
        RequestQuota(
            limit=-1,
            window_seconds=60,
        )


def test_rejects_zero_window():
    with pytest.raises(InvalidQuotaError):
        RequestQuota(
            limit=100,
            window_seconds=0,
        )


def test_rejects_negative_window():
    with pytest.raises(InvalidQuotaError):
        RequestQuota(
            limit=100,
            window_seconds=-1,
        )


def test_is_immutable():
    quota = RequestQuota(
        limit=100,
        window_seconds=60,
    )

    with pytest.raises(AttributeError):
        quota.limit = 200