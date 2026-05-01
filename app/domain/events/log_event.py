# app/domain/events/log_event.py

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class LogEvent:
    """
    Domain Event: rappresenta un evento rilevante nel sistema.
    NON conosce Mongo, JSON o dettagli di persistenza.
    """

    event_type: str
    message: str
    client_ip: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        """
        Conversione generica (non Mongo-specifica)
        """
        return {
            "event_type": self.event_type,
            "message": self.message,
            "client_ip": self.client_ip,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }