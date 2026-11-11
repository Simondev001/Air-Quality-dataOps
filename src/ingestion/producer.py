"""Generate and publish simulated air-quality events to Kafka."""

import json
import logging
import math
import os
import random
import time
from datetime import datetime, timezone
from typing import Optional

from src.ingestion.schemas import AirQualityEvent

LOGGER = logging.getLogger(__name__)

SENSORS = {
    "sensor-paris-01": ("Paris centre", 12.0, 24.0, 18.0, 22.0, 16.0, 55.0),
    "sensor-paris-02": ("Paris nord", 10.0, 21.0, 15.0, 20.0, 15.0, 58.0),
    "sensor-lyon-01": ("Lyon centre", 11.0, 23.0, 17.0, 21.0, 17.0, 52.0),
}


def generate_event(
    now: Optional[datetime] = None,
    rng: Optional[random.Random] = None,
) -> AirQualityEvent:
    """Generate a daily-cycle reading with occasional missing or unusual values."""
    random_source = rng or random.Random()
    current_time = now or datetime.now(timezone.utc)
    if current_time.tzinfo is None:
        raise ValueError("now must be timezone-aware")

    sensor_id = random_source.choice(list(SENSORS))
    location, pm25_base, pm10_base, no2_base, o3_base, temp_base, humidity_base = SENSORS[sensor_id]
    hour = current_time.hour + current_time.minute / 60
    rush_hour = max(0.0, math.cos((hour - 8) * math.pi / 12))
    daylight = max(0.0, math.sin((hour - 6) * math.pi / 12))

    values: dict[str, Optional[float]] = {
        "pm25": max(0.0, random_source.gauss(pm25_base + 8 * rush_hour, 3)),
        "pm10": max(0.0, random_source.gauss(pm10_base + 12 * rush_hour, 5)),
        "no2": max(0.0, random_source.gauss(no2_base + 14 * rush_hour, 4)),
        "o3": max(0.0, random_source.gauss(o3_base + 12 * daylight, 5)),
        "temperature": random_source.gauss(temp_base + 5 * daylight, 2),
        "humidity": min(100.0, max(0.0, random_source.gauss(humidity_base - 8 * daylight, 6))),
    }

    if random_source.random() < 0.04:
        # Pollution episodes affect several pollutant readings together.
        for pollutant in ("pm25", "pm10", "no2"):
            if values[pollutant] is not None:
                values[pollutant] *= random_source.uniform(2.0, 4.0)
    if random_source.random() < 0.01:
        # A sensor fault can produce a physically implausible spike.
        outlier = random_source.choice(("pm25", "pm10", "no2", "o3", "temperature", "humidity"))
        values[outlier] = random_source.choice((-999.0, 9999.0))
    for field in values:
        if random_source.random() < 0.015:
            values[field] = None

    return AirQualityEvent(
        sensor_id=sensor_id,
        timestamp=current_time.astimezone(timezone.utc).isoformat(),
        location=location,
        **values,
    )


def publish_forever() -> None:
    """Connect to Kafka and publish simulated events until interrupted."""
    try:
        from kafka import KafkaProducer
    except ImportError as exc:
        raise RuntimeError("Install project dependencies with: pip install -r requirements.txt") from exc

    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = os.getenv("KAFKA_TOPIC", "raw_data")
    interval = float(os.getenv("PRODUCER_INTERVAL_SECONDS", "1"))
    if interval <= 0:
        raise ValueError("PRODUCER_INTERVAL_SECONDS must be greater than zero")

    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers.split(","),
        value_serializer=lambda event: json.dumps(event, allow_nan=False).encode("utf-8"),
        retries=5,
    )
    LOGGER.info("Publishing events to topic '%s' at %s", topic, bootstrap_servers)
    try:
        while True:
            event = generate_event()
            future = producer.send(topic, event.to_dict())
            metadata = future.get(timeout=10)
            LOGGER.info("Published sensor event to %s partition %d offset %d", metadata.topic, metadata.partition, metadata.offset)
            time.sleep(interval)
    finally:
        producer.flush(timeout=10)
        producer.close(timeout=10)


if __name__ == "__main__":
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    try:
        publish_forever()
    except KeyboardInterrupt:
        LOGGER.info("Producer stopped")
