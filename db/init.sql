CREATE TABLE IF NOT EXISTS _meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

INSERT INTO _meta (key, value)
VALUES ('schema_version', '0.1.0')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;
