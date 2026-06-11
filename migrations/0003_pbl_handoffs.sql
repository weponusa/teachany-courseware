CREATE TABLE IF NOT EXISTS pbl_handoffs (
  id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  expires_at TEXT NOT NULL,
  goal TEXT NOT NULL,
  payload_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_pbl_handoffs_expires ON pbl_handoffs(expires_at);
