# Binary‑Rogue Overview

Binary‑Rogue is a deterministic system for evaluating external signals and producing ranked, static outputs suitable for immediate consumption.

The system prioritizes **clarity, speed, and repeatability** over interactivity or autonomy.

---

## High‑Level Flow

1. **Acquire** — Ingestion adapters fetch external signals from various sources
2. **Interpret** — Semantic meaning and normalization applied to raw signals
3. **Consolidate** — Related signals grouped into story candidates
4. **Value** — Stories ranked and optimal placements selected
5. **Verify** — Confidence reduced where anomalies or contradictions exist
6. **Emit** — Static artifacts written atomically to output directory

Each step is deterministic, side-effect free, and explicitly orchestrated.

---

## Execution Characteristics

- Batch‑oriented
- Side‑effect free evaluation
- No runtime learning or adaptation
- No persistent agent state
- No client‑side logic beyond rendering

---

## Documentation Roadmap

For first-time readers, follow this order:

1. **OVERVIEW.md** (this file) — System philosophy and execution model
2. **ARCHITECTURE.md** — Three-layer structure and boundaries
3. **INGESTION.md** — How external signals are acquired
4. **DATA_INTELLIGENCE.md** — Core terminology and semantics
5. **EVALUATORS.md** — Intelligence layer building blocks
6. **OUTPUTS.md** — Static artifact specification
7. **FRONTEND.md** — Visual contract and rendering rules
8. **BUILD.md** — Build lifecycle and phases
9. **PERSISTENCE.md** — Optional database schema
10. **OPERATIONS.md** — Deployment and runtime
11. **SECURITY.md** — Security constraints
12. **VERSIONING.md** — Compatibility policy
13. **REFERENCE_RUNTIME.md** — Illustrative execution model

For technical integration:
- Start with **OUTPUTS.md** for artifact schema
- Review **EVALUATORS.md** for intelligence interfaces
- Check **SECURITY.md** for safety requirements

---

## Design Intent

Binary‑Rogue is optimized for environments where:

- Outputs must be reproducible
- Behavior must be explainable
- Changes must be intentional and reviewable
- Runtime complexity increases operational risk

---

## Design Rationale

### Why Deterministic?

**Problem:** Non‑deterministic systems make debugging, auditing, and compliance verification nearly impossible.

**Solution:** Binary‑Rogue guarantees that identical inputs produce identical outputs. This enables:

- **Reproducible debugging** — Run the same build locally to investigate issues
- **Audit compliance** — Prove outputs match documented logic
- **Change verification** — Test modifications with known datasets
- **Confidence in production** — Eliminate "works on my machine" scenarios

### Why Static Outputs?

**Problem:** Dynamic, personalized systems require complex backend infrastructure, introduce security risks, and make content moderation difficult.

**Solution:** Generate static JSON artifacts that are:

- **Cacheable** — CDN-friendly, fast global distribution
- **Auditable** — Complete artifact snapshot at any point in time
- **Secure** — No server-side processing, minimal attack surface
- **Simple** — Standard HTTP file serving, no special infrastructure
- **Versioned** — Each build is an immutable artifact

### Why Three Lanes?

**Problem:** Flat lists make prioritization unclear and force readers to process everything sequentially.

**Solution:** Three lanes (`signal`, `wire`, `flash`) provide natural content tiers:

- **signal** — Top weighted stories, primary attention
- **wire** — Secondary important stories, secondary attention
- **flash** — Breaking/urgent stories, time-sensitive attention

This structure guides user attention without requiring client-side logic.

### Why Batch Processing?

**Problem:** Streaming systems require constant connection, complex state management, and introduce operational complexity.

**Solution:** Periodic batch builds:

- **Predictable resource usage** — Bounded compute, scheduled execution
- **Complete context** — Full dataset available for ranking decisions
- **Operational simplicity** — Standard cron job, no complex orchestration
- **Quality over speed** — Time to apply sophisticated evaluators

Most use cases don't require sub-minute updates; 15-minute builds are sufficient.

### Why No Client-Side Intelligence?

**Problem:** Client-side intelligence creates inconsistent experiences, complicates debugging, and makes behavior unpredictable.

**Solution:** All intelligence runs server-side:

- **Consistent experience** — Every user sees the same prioritization
- **Centralized quality control** — One place to improve algorithms
- **Simple clients** — Render JSON, no complex logic
- **Reduced attack surface** — No sensitive logic exposed to clients

### Why Symmetric Sentiment Scoring?

**Problem:** Asymmetric scales (0-10, 1-5) obscure neutral sentiment and make interpretation context-dependent.

**Solution:** Symmetric -2 to +2 range:

- **Clear neutral** — 0 is unambiguously neutral
- **Intuitive magnitude** — Distance from 0 indicates strength
- **Balanced representation** — Equal range for positive and negative
- **Simple thresholds** — Easy to categorize (negative < 0, positive > 0)

---

## Explicit Non‑Goals

Binary‑Rogue intentionally does **not** provide:

- Streaming or real‑time personalization
- Interactive filtering or tuning
- Autonomous agents or delegated authority
- Self‑modifying or feedback‑driven logic
- Client‑side intelligence

These exclusions are design choices, not limitations.
