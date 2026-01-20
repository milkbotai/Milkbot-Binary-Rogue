# Data & Intelligence Semantics

This document defines what Binary‑Rogue **means** when it uses specific terms. These semantics are v1.0‑stable.

## Signal

A **signal** is an atomic input item that may refer to a real‑world event or development.

Signals are raw inputs. They are not yet merged, ranked, or rewritten for prominence.

## Story

A **story** is an inferred representation of a real‑world event or development derived by consolidating multiple signals.

Stories are contextual to a build window. Persistence may retain story state for history, but the system does not assume permanence.

## Cluster (Story‑Level Property)

A **cluster** is a transient grouping property computed during a build.

- Clusters are not durable entities.
- Membership may vary across builds.
- Cluster properties inform valuation.

Conceptual properties:

- `cluster_size` — number of supporting signals
- `diversity_count` — number of distinct sources
- `temporal_density` — concentration in time
- `consensus_strength` — inferred agreement across sources

## Symmetric Scoring (‑2 → +2)

Binary‑Rogue uses a symmetric ordinal scoring range for quality and sentiment‑like values:

- **‑2**: actively harmful / misleading
- **‑1**: low quality / noisy / unreliable
- **0**: neutral / unknown / unproven
- **+1**: reliable / consistent
- **+2**: exceptional / authoritative

The scale is **ordinal** and **directional**, not probabilistic.

## Source Quality vs Transport Quality

- **Source quality** describes the origin’s reliability.
- **Transport quality** describes the acquisition channel’s reliability.

Both can influence valuation without changing a signal’s meaning.

## Identity and Determinism

Stable IDs should be deterministically derived from canonical inputs.

Suggested identity inputs:

- `source_id`: canonical domain or registry key
- `signal_id`: canonical URL + published timestamp + source_id
- `story_id`: consolidation signature (canonical family + semantic fingerprint)
