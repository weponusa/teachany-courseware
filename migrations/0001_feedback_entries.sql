CREATE TABLE IF NOT EXISTS feedback_entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  course_id TEXT NOT NULL,
  course_name TEXT,
  node_id TEXT,
  subject TEXT,
  grade TEXT,
  learner_name TEXT,
  class_name TEXT,
  understood INTEGER,
  difficulty TEXT,
  pre_score REAL,
  post_score REAL,
  hardest_part TEXT,
  reflection TEXT,
  contact TEXT,
  user_agent TEXT,
  ip_hash TEXT,
  raw_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_feedback_course_id ON feedback_entries(course_id);
CREATE INDEX IF NOT EXISTS idx_feedback_created_at ON feedback_entries(created_at);
