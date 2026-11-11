import json
import random
import unittest
from datetime import datetime, timezone

from src.ingestion.producer import generate_event
from src.ingestion.schemas import AirQualityEvent


class AirQualityEventTests(unittest.TestCase):
    def test_event_requires_timezone_aware_timestamp(self) -> None:
        with self.assertRaisesRegex(ValueError, "include a timezone"):
            AirQualityEvent(
                sensor_id="sensor-1",
                timestamp="2026-11-09T12:00:00",
                location="Paris",
                pm25=None,
                pm10=None,
                no2=None,
                o3=None,
                temperature=None,
                humidity=None,
            )

    def test_missing_readings_are_serialized_as_json_null(self) -> None:
        event = AirQualityEvent(
            sensor_id="sensor-1",
            timestamp="2026-11-09T12:00:00+00:00",
            location="Paris",
            pm25=None,
            pm10=12.0,
            no2=3.0,
            o3=4.0,
            temperature=18.0,
            humidity=50.0,
        )

        payload = json.loads(json.dumps(event.to_dict(), allow_nan=False))
        self.assertIsNone(payload["pm25"])
        self.assertEqual(payload["sensor_id"], "sensor-1")

    def test_generator_emits_complete_timestamped_event(self) -> None:
        event = generate_event(
            now=datetime(2026, 11, 9, 12, tzinfo=timezone.utc),
            rng=random.Random(7),
        )

        self.assertTrue(event.sensor_id.startswith("sensor-"))
        self.assertEqual(event.timestamp, "2026-11-09T12:00:00+00:00")
        self.assertTrue(event.location)
        self.assertEqual(
            set(event.to_dict()),
            {"sensor_id", "timestamp", "location", "pm25", "pm10", "no2", "o3", "temperature", "humidity"},
        )

    def test_generator_rejects_naive_clock(self) -> None:
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            generate_event(now=datetime(2026, 11, 9, 12))


if __name__ == "__main__":
    unittest.main()
