CREATE TABLE IF NOT EXISTS pbl_llm_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  stage TEXT NOT NULL,
  goal TEXT NOT NULL,
  model TEXT,
  backend TEXT,
  complex INTEGER DEFAULT 0,
  latency_ms INTEGER,
  error TEXT,
  messages_json TEXT,
  response_text TEXT,
  user_agent TEXT,
  ip_hash TEXT
);

CREATE INDEX IF NOT EXISTS idx_pbl_logs_created_at ON pbl_llm_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_pbl_logs_stage ON pbl_llm_logs(stage);
CREATE INDEX IF NOT EXISTS idx_pbl_logs_goal ON pbl_llm_logs(goal);
