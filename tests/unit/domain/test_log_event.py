# tests/unit/domain/test_log_event.py

from app.domain.events.log_event import LogEvent


def test_should_create_log_event():
    event = LogEvent(
        event_type="RATE_LIMIT_EXCEEDED",
        message="Too many requests",
        client_ip="127.0.0.1",
        metadata={"count": 10}
    )

    assert event.event_type == "RATE_LIMIT_EXCEEDED"
    assert event.client_ip == "127.0.0.1"
    assert event.metadata["count"] == 10


def test_should_have_timestamp():
    event = LogEvent(
        event_type="INFO",
        message="ok"
    )

    assert event.occurred_at is not None