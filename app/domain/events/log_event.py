# app/domain/events/log_event.py

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class LogEvent:
    event_type: str
    message: str
    client_ip: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )