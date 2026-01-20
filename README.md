
# Binary‑Rogue

**Binary‑Rogue is a deterministic signal evaluation and story‑prioritization system.**

This repository defines the **canonical v1.0 specification and contracts** for Binary‑Rogue. It establishes architectural boundaries, data semantics, evaluator behavior, schema guarantees, and operational constraints.

This repository **does not provide a required runtime implementation**.

Binary‑Rogue intentionally avoids autonomous behavior, runtime decision loops, and client‑side intelligence. All outputs are produced through explicitly defined, deterministic processes and emitted as static artifacts.

---

## What This Repository Is

- The authoritative specification for Binary‑Rogue v1.0
- A schema‑first definition of inputs, outputs, and invariants
- Documentation intended to be machine‑verifiable and auditable
- A baseline suitable for enterprise and regulated environments

## What This Repository Is Not

- A long‑running service
- An autonomous or agent‑based system
- A dynamic or adaptive application
- A client‑side intelligent system

---

## Core Properties

- **Determinism:** identical inputs produce materially identical outputs
- **Static outputs:** results are emitted as immutable artifacts
- **Separation of concerns:** ingestion, evaluation, and presentation are strictly bounded
- **Auditability:** evaluation decisions can be traced to explicit inputs and evaluators

---

## Documentation

See `docs/OVERVIEW.md` for the system overview and execution model, then follow the documentation map defined there.
