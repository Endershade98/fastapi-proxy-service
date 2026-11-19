# tests/unit/domain/events/test_rate_limit.py

from datetime import datetime, timezone

import pytest

from app.domain.events.rate_limit import RateLimitExceeded
from app.domain.value_objects.client_ip import ClientIP
from app.domain.value_objects.request_quota import RequestQuota


def test_creates_rate_limit_exceeded_event():
    occurred_at = datetime.now(timezone.utc)
    client_ip = ClientIP("192.168.1.10")
    quota = RequestQuota(
        limit=100,
        window_seconds=60,
    )

    event = RateLimitExceeded(
        client_ip=client_ip,
        quota=quota,
        occurred_at=occurred_at,
    )

    assert event.client_ip == client_ip
    assert event.quota == quota
    assert event.occurred_at == occurred_at


def test_event_is_immutable():
    event = RateLimitExceeded(
        client_ip=ClientIP("127.0.0.1"),
        quota=RequestQuota(
            limit=10,
            window_seconds=60,
        ),
        occurred_at=datetime.now(timezone.utc),
    )

    with pytest.raises(AttributeError):
        event.client_ip = ClientIP("10.0.0.1")