# tests/unit/domain/test_request_quota.py

import pytest

from app.domain.value_objects.request_quota import RequestQuota
from app.domain.exceptions import InvalidQuotaError


def test_should_create_valid_quota():
    quota = RequestQuota(limit=10, window_seconds=60)

    assert quota.limit == 10
    assert quota.window_seconds == 60


@pytest.mark.parametrize("limit,window", [
    (0, 60),
    (-1, 60),
    (10, 0),
    (10, -5),
])
def test_should_reject_invalid_values(limit, window):
    with pytest.raises(InvalidQuotaError):
        RequestQuota(limit=limit, window_seconds=window)