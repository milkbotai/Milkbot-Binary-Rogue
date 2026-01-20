# Architecture

Binary‑Rogue is structured as three explicit layers with strict authority boundaries.

## Layer 1 — Ingestion

**Job**: acquire external signals and normalize them.

**Rules**:

- Adapters are transport‑agnostic and replaceable.
- Ingestion does **not** rank, merge, or decide importance.
- Ingestion preserves provenance for every signal.

**Output**: normalized signals suitable for evaluator processing.

## Layer 2 — Intelligence

**Job**: apply composed judgments to produce prioritized story candidates.

Intelligence is expressed as evaluator stages:

- **Interpretation** — semantic meaning and normalization
- **Consolidation** — grouping signals into story candidates
- **Valuation** — ranking and placement
- **Verification** — confidence reduction when anomalies exist

No single evaluator is authoritative. The system’s behavior emerges from the composition of partial judgments.

## Layer 3 — Presentation

**Job**: emit static artifacts for consumption.

**Rules**:

- Presentation performs no intelligence decisions.
- Artifacts are read‑only views.
- Artifact writes are atomic.

## Determinism

A build is deterministic when the following are deterministic:

- input normalization
- evaluator configurations
- stable ID derivation
- stable sorting and tie‑breakers
- schema versioning

## Extensibility

Binary‑Rogue evolves by:

- adding ingestion adapters
- adding/replacing evaluator implementations
- adding optional persistence
- adding new artifacts with explicit schema versioning
