# Persistence (Optional)

Binary‑Rogue can run without a database. When present, persistence provides:

- History (what happened over time)
- Caching (avoid re‑evaluation)
- Quality memory (source performance and trust)
- Auditability (why a decision was made)

Persistence must never be required to render the frontend.

## Conceptual Schema Direction (SQLite‑Friendly)

Clusters are story‑level properties. If persisted, store cluster fields on the story row.

```sql
CREATE TABLE IF NOT EXISTS sources (
  source_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  domain TEXT,
  quality_score INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL,
  last_seen_at TEXT
);

CREATE TABLE IF NOT EXISTS signals (
  signal_id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL,
  canonical_url TEXT,
  title TEXT,
  summary TEXT,
  published_at TEXT,
  observed_at TEXT NOT NULL,
  transport TEXT,
  raw_hash TEXT,
  FOREIGN KEY (source_id) REFERENCES sources(source_id)
);

CREATE TABLE IF NOT EXISTS stories (
  story_id TEXT PRIMARY KEY,
  first_seen_at TEXT NOT NULL,
  last_seen_at TEXT NOT NULL,
  cluster_size INTEGER NOT NULL DEFAULT 1,
  diversity_count INTEGER NOT NULL DEFAULT 1,
  valuation_weight INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS story_signals (
  story_id TEXT NOT NULL,
  signal_id TEXT NOT NULL,
  PRIMARY KEY (story_id, signal_id)
);

CREATE TABLE IF NOT EXISTS build_runs (
  build_id TEXT PRIMARY KEY,
  started_at TEXT NOT NULL,
  completed_at TEXT,
  schema_version TEXT NOT NULL
);
```
