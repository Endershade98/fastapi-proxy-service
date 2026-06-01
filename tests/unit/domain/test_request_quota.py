# tests/unit/domain/test_request_quota.py

import pytest
from app.domain.value_objects.request_quota import RequestQuota
from app.domain.exceptions import InvalidQuotaError


def test_valid_quota():
    q = RequestQuota(limit=10, window_seconds=60)
    assert q.limit == 10


def test_invalid_quota():
    with pytest.raises(InvalidQuotaError):
        RequestQuota(limit=0, window_seconds=10)