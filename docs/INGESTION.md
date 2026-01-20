# Ingestion

Ingestion turns external inputs into normalized signals.

Binary‑Rogue treats ingestion as adapters. Each adapter implements the same conceptual contract.

## Adapter Contract

An ingestion adapter must:

- acquire raw inputs
- normalize into signal objects
- emit provenance and acquisition metadata

An ingestion adapter must not:

- rewrite content for presentation
- apply sentiment or importance judgment
- merge items into stories

## Normalized Signal (Conceptual Fields)

- `signal_id` — stable, deterministic
- `source_id` — stable identity for the origin
- `source_name` — display label
- `canonical_url` — preferred link (if applicable)
- `title` — short descriptor
- `summary` — optional
- `published_at` — origin timestamp when available
- `observed_at` — adapter observation timestamp
- `transport` — adapter identifier
- `raw_ref` — optional pointer/hash for traceability

## Provenance Rules

Provenance enables quality scoring, debugging, and auditability.

At minimum, provenance includes `source_id` and `transport`.

## Canonicalization Guidance

Adapters should normalize tracking parameters and prefer canonical URLs without making intelligence decisions.
