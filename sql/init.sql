CREATE TABLE IF NOT EXISTS sensors (
    sensor_id TEXT PRIMARY KEY,
    location TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS air_quality_measurements (
    measurement_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sensor_id TEXT NOT NULL REFERENCES sensors(sensor_id),
    measured_at TIMESTAMPTZ NOT NULL,
    location TEXT NOT NULL,
    pm25 DOUBLE PRECISION,
    pm10 DOUBLE PRECISION,
    no2 DOUBLE PRECISION,
    o3 DOUBLE PRECISION,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_measurement_sensor_time UNIQUE (sensor_id, measured_at)
);

CREATE INDEX IF NOT EXISTS idx_measurements_measured_at
    ON air_quality_measurements (measured_at DESC);
CREATE INDEX IF NOT EXISTS idx_measurements_sensor_time
    ON air_quality_measurements (sensor_id, measured_at DESC);

CREATE TABLE IF NOT EXISTS anomalies (
    anomaly_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    measurement_id BIGINT NOT NULL REFERENCES air_quality_measurements(measurement_id) ON DELETE CASCADE,
    detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    rule_name TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    description TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_anomalies_detected_at
    ON anomalies (detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_anomalies_measurement
    ON anomalies (measurement_id);

CREATE TABLE IF NOT EXISTS model_predictions (
    prediction_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sensor_id TEXT REFERENCES sensors(sensor_id),
    predicted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    prediction TEXT NOT NULL,
    anomaly_score DOUBLE PRECISION,
    input_features JSONB NOT NULL DEFAULT '{}'::JSONB
);

CREATE INDEX IF NOT EXISTS idx_predictions_predicted_at
    ON model_predictions (predicted_at DESC);
CREATE INDEX IF NOT EXISTS idx_predictions_sensor_time
    ON model_predictions (sensor_id, predicted_at DESC);
