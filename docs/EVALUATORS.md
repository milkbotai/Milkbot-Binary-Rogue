# Evaluators

Evaluators are the intelligence layer’s building blocks. Each evaluator is a specialized judgment stage with explicit inputs, outputs, and failure behavior.

Binary‑Rogue is intentionally model‑agnostic.

## Core Principle

Models are implementation details of evaluators. Evaluator contracts are the stable surface.

## Evaluator Interface (Conceptual)

### Inputs

- `signals`: one signal or a set of signals
- `context`: optional structured context (quality memory, cached decisions, historical summaries)
- `constraints`: optional limits (time budget, compute budget)

### Outputs

- `annotations`: structured metadata additions
- `confidence`: ordinal or categorical
- `warnings`: non‑fatal issues
- `errors`: fatal issues

### Failure Behavior

- **Hard fail**: return errors; emit no annotations.
- **Soft fail**: emit degraded annotations; include warnings.

Evaluators must not fabricate required fields when the input lacks sufficient information.

## Evaluator Types

### Interpretation

Determines semantic meaning.

Typical outputs:

- normalized headlines (`headline_caps`, `headline_title`)
- topical tags
- entity hints

### Consolidation

Groups related signals into story candidates.

Typical outputs:

- derived `story_id`
- mapping (signal → story)
- story‑level cluster properties

### Valuation

Ranks stories and selects placements.

Typical outputs:

- `weight` per story
- placement decisions (ALERT vs lanes)
- boosts/penalties using recency, diversity, and quality scores

### Verification (Negative Capability)

Reduces confidence when anomalies exist.

Typical outputs:

- contradiction flags
- structural validity flags
- down‑weight recommendations

## Composition

Composition is explicit and configurable:

- Interpretation runs on raw signals.
- Consolidation runs on interpreted signals.
- Valuation runs on story candidates.
- Verification may run at multiple points.
