# tests/unit/application/logging/test_publish_event.py

import pytest

from app.application.logging.use_cases.publish_event import (
    PublishEventUseCase,
)


class FakeEventPublisher:
    def __init__(self):
        self.events = []

    async def publish(self, event):
        self.events.append(event)


@pytest.mark.asyncio
async def test_publishes_event():
    publisher = FakeEventPublisher()

    use_case = PublishEventUseCase(
        publisher=publisher,
    )

    event = {
        "event_type": "test",
        "value": 123,
    }

    await use_case.execute(event)

    assert publisher.events == [event]


@pytest.mark.asyncio
async def test_propagates_publisher_exception():
    class FailingPublisher:
        async def publish(self, event):
            raise RuntimeError("publisher failed")

    use_case = PublishEventUseCase(
        publisher=FailingPublisher(),
    )

    with pytest.raises(RuntimeError, match="publisher failed"):
        await use_case.execute({"event": "test"})