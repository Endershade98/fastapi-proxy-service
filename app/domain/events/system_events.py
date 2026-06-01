# app/domain/events/system_events.py

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class RequestLoggedEvent:
    event_type: str
    path: str
    client_ip: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class RateLimitExceededEvent:
    client_ip: str
    limit: int
    window_seconds: int
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))