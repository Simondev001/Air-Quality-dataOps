"""Shared event contract for raw air-quality measurements."""

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class AirQualityEvent:
    """One sensor reading. Sensor values may be null in the raw topic."""

    sensor_id: str
    timestamp: str
    location: str
    pm25: Optional[float]
    pm10: Optional[float]
    no2: Optional[float]
    o3: Optional[float]
    temperature: Optional[float]
    humidity: Optional[float]

    def __post_init__(self) -> None:
        if not self.sensor_id.strip():
            raise ValueError("sensor_id must not be empty")
        if not self.location.strip():
            raise ValueError("location must not be empty")
        try:
            parsed_timestamp = datetime.fromisoformat(self.timestamp.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("timestamp must be an ISO 8601 datetime") from exc
        if parsed_timestamp.tzinfo is None:
            raise ValueError("timestamp must include a timezone")

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation of the event."""
        return asdict(self)
