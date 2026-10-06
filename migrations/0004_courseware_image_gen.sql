-- TeachAny 课件生图中转配额（Agnes 免费生图，每课件默认 3 张）
-- 在 TEACHANY_DB 执行：migrations/0004_courseware_image_gen.sql

CREATE TABLE IF NOT EXISTS courseware_image_quota (
  course_id TEXT PRIMARY KEY,
  used_count INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS courseware_image_gen_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  course_id TEXT NOT NULL,
  slot TEXT,
  prompt TEXT,
  size TEXT,
  remote_url TEXT,
  latency_ms INTEGER,
  error TEXT,
  ip_hash TEXT,
  user_agent TEXT
);

CREATE INDEX IF NOT EXISTS idx_img_logs_course ON courseware_image_gen_logs(course_id);
CREATE INDEX IF NOT EXISTS idx_img_logs_created_at ON courseware_image_gen_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_img_logs_ip_hash ON courseware_image_gen_logs(ip_hash);
