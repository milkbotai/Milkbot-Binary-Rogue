# Build Lifecycle

A build is a single evaluation pass that produces a coherent set of artifacts.

Each build executes six deterministic phases in sequence. The entire lifecycle targets completion within 60 seconds for typical workloads.

---

## Build Phases

### 1. Acquire

**Purpose:** Fetch and normalize external signals into a consistent format.

**Process:**
- Ingestion adapters connect to configured sources
- Raw data is fetched (RSS feeds, APIs, webhooks, files)
- Each signal is normalized to standard schema
- Duplicate signals are identified and merged
- Timestamp and source metadata attached

**Output:** Normalized signal collection

**Target Duration:** < 10 seconds for 1000 signals

**Failure Handling:**
- Individual adapter failures are logged but don't halt the build
- Partial signal sets are acceptable
- Network timeouts use exponential backoff (max 3 retries)

---

### 2. Interpret

**Purpose:** Apply semantic understanding to raw signals.

**Process:**
- Extract entities (companies, technologies, people, places)
- Assign initial sentiment scores
- Identify signal topics and categories
- Tag breaking vs. routine content
- Compute signal quality metrics

**Output:** Semantically annotated signals

**Target Duration:** < 5 seconds for 1000 signals

**Evaluators Used:**
- Entity extraction
- Sentiment analysis
- Topic classification
- Quality scoring

---

### 3. Consolidate

**Purpose:** Group related signals into story candidates.

**Process:**
- Cluster signals by semantic similarity
- Merge duplicate or near‑duplicate content
- Select representative headline for each cluster
- Compute cluster size and coherence metrics
- Assign provisional story confidence

**Output:** Story candidates with cluster metadata

**Target Duration:** < 8 seconds for 1000 signals → ~200 stories

**Clustering Strategy:**
- Similarity threshold: 0.75 (cosine similarity)
- Minimum cluster size: 1 (singleton stories allowed)
- Maximum cluster size: unbounded

---

### 4. Value

**Purpose:** Rank stories and determine optimal placements.

**Process:**
- Compute story weight from multiple signals:
  - Recency (more recent = higher weight)
  - Source authority (trusted sources = higher weight)
  - Cluster size (more sources = higher weight)
  - Sentiment magnitude (stronger sentiment = higher weight)
  - Breaking news indicators (breaking = higher weight)
- Sort stories by weight descending
- Select top N stories for each lane
- Identify alert candidate (highest weight overall)
- Populate ticker buckets with relevant data

**Output:** Ranked and placed stories

**Target Duration:** < 3 seconds

**Placement Rules:**
- **signal:** Top 3-5 weighted stories
- **wire:** Next 2-4 weighted stories
- **flash:** Recent breaking stories (< 2 hours old)
- **alert:** Single highest‑weight story (if weight > threshold)

---

### 5. Verify

**Purpose:** Reduce confidence where anomalies or inconsistencies exist.

**Process:**
- Check for contradictory signals within clusters
- Verify source reliability
- Detect potential misinformation patterns
- Flag outlier sentiment scores
- Validate entity consistency
- Check temporal coherence

**Output:** Confidence‑adjusted stories

**Target Duration:** < 2 seconds

**Confidence Adjustments:**
- Contradictory sources: −20% confidence
- Low‑reliability sources: −30% confidence
- Outlier sentiment: −15% confidence
- Failed fact checks: −50% confidence

Stories below 50% confidence may be demoted or removed.

---

### 6. Emit

**Purpose:** Write final artifacts atomically and consistently.

**Process:**
- Serialize stories to JSON format
- Validate against schema
- Generate build metadata (timestamp, build ID, version)
- Write artifact atomically (tmp file → rename)
- Verify artifact integrity
- Update index/manifest if maintaining history

**Output:** Static JSON artifact (`headlines.json`)

**Target Duration:** < 2 seconds

**Atomicity Guarantee:**
- Write to temporary file first
- Validate before rename
- Atomic rename operation
- Never expose partial artifacts

---

## Performance Benchmarks

### Target Performance (Typical Load)

| Phase | Target | Maximum |
|-------|--------|---------|
| Acquire | < 10s | 30s |
| Interpret | < 5s | 15s |
| Consolidate | < 8s | 20s |
| Value | < 3s | 10s |
| Verify | < 2s | 5s |
| Emit | < 2s | 5s |
| **Total** | **< 30s** | **60s** |

### Load Scenarios

**Light Load (< 100 signals):**
- Total time: < 10 seconds
- All phases complete quickly
- Suitable for frequent builds (every 5 minutes)

**Typical Load (100-500 signals):**
- Total time: < 30 seconds
- Most production scenarios
- Suitable for regular builds (every 15 minutes)

**Heavy Load (500-1000 signals):**
- Total time: < 45 seconds
- High‑volume news days
- May require rate limiting on sources

**Stress Load (> 1000 signals):**
- Total time: < 60 seconds (target), < 90 seconds (maximum)
- Breaking news events, crises
- May need to sample or prioritize sources

### Performance Monitoring

Implementations should log:
- Phase duration for each build
- Signal counts per phase
- Evaluator timing breakdown
- Source fetch latency
- Schema validation time

---

## Determinism

A build is deterministic given:
- Same normalized input signals
- Same evaluator configuration
- Same system time (or fixed timestamp)
- Same schema version

**Determinism Verification:**

Run the same build twice:
```bash
# Build 1
./build --input signals.json --output output1.json --timestamp 2026-01-18T14:00:00Z

# Build 2 (same inputs)
./build --input signals.json --output output2.json --timestamp 2026-01-18T14:00:00Z

# Compare
diff output1.json output2.json
# Should be identical (exit code 0)
```

**Sources of Non‑Determinism to Avoid:**
- Random number generators without fixed seeds
- System timestamp calls (use parameter instead)
- Hash map iteration order (use sorted iteration)
- Floating‑point non‑associativity (use stable sorting)
- Concurrent execution without ordering guarantees

---

## Build Metadata

Every build must emit metadata sufficient for audit and debugging.

### Required Metadata

```json
{
  "meta": {
    "schema_version": "1.0",
    "generated_at": "2026-01-18T14:30:00Z",
    "build_id": "20260118-1430-a3f7b2c1",
    "sources_observed": 12,
    "signals_ingested": 427,
    "stories_created": 156,
    "evaluators_used": [
      "sentiment_v1",
      "entity_extraction_v2",
      "clustering_v1"
    ],
    "build_duration_ms": 28450,
    "phase_timing": {
      "acquire_ms": 8234,
      "interpret_ms": 4891,
      "consolidate_ms": 7123,
      "value_ms": 2456,
      "verify_ms": 1892,
      "emit_ms": 1854
    }
  }
}
```

### Audit Questions Answered

With proper metadata, you can answer:

- **What sources were observed?** → `sources_observed`, source list
- **What evaluators ran?** → `evaluators_used`
- **What schema version?** → `schema_version`
- **Why was this story selected?** → Weight calculation + evaluator scores
- **How long did the build take?** → `build_duration_ms`, `phase_timing`
- **When was it generated?** → `generated_at`
- **Is this deterministic?** → `build_id` encodes inputs

---

## Build Scheduling

### Recommended Schedule

- **Production:** Every 15 minutes
- **Development:** Every 30 minutes
- **Testing:** On demand

### Triggering Mechanisms

Builds can be triggered by:
1. **Scheduled cron job** (recommended for production)
2. **Webhook on source update** (real‑time scenarios)
3. **Manual invocation** (testing, debugging)
4. **API request** (programmatic control)

### Build Coordination

For high‑availability deployments:
- Only one build should run at a time
- Use distributed lock (Redis, etcd, file lock)
- Failed builds release lock automatically (timeout)
- New builds wait for previous completion

---

## Error Handling

### Partial Failures

Builds should complete even with partial failures:
- Some sources unavailable → Proceed with available signals
- Evaluator fails → Skip that evaluator, log warning
- Low signal count → Generate minimal output
- Network timeout → Retry with backoff, then proceed

### Complete Failures

Builds should abort if:
- Zero signals acquired (all sources failed)
- Schema validation fails
- Output write fails
- Critical evaluator fails (if marked as required)

### Failure Recovery

On failure:
1. Log complete error context
2. Preserve input signals for debugging
3. Do not overwrite previous good artifact
4. Alert monitoring system
5. Retry with exponential backoff (if transient)

---

## Build Optimization

### Performance Tips

1. **Parallel ingestion** – Fetch from multiple sources concurrently
2. **Batch evaluators** – Process signals in batches, not one‑by‑one
3. **Cache embeddings** – Reuse semantic vectors for duplicate content
4. **Incremental processing** – Skip unchanged signals when possible
5. **Early filtering** – Discard low‑quality signals before expensive ops

### Monitoring Build Health

Track these metrics over time:
- Average build duration trend
- Signal count trend
- Story count trend
- Phase timing distribution
- Failure rate by source
- Evaluator performance

Alert when:
- Build duration > 60 seconds (3 consecutive builds)
- Signal count drops > 50% from baseline
- Failure rate > 20%
- Any phase > 2x target duration

---

## Build Configuration

### Configuration Parameters

```yaml
build:
  max_signals: 1000
  timeout_seconds: 90
  parallel_sources: 5
  
phases:
  acquire:
    timeout_per_source: 10
    retry_count: 3
    retry_backoff_ms: 1000
  
  consolidate:
    similarity_threshold: 0.75
    min_cluster_size: 1
  
  value:
    alert_weight_threshold: 85
    max_signal_stories: 5
    max_wire_stories: 4
    max_flash_stories: 3
```

---

This build lifecycle ensures Binary‑Rogue produces high‑quality, deterministic artifacts efficiently and reliably.
