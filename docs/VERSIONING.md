
# Versioning and Compatibility Policy

Binary‑Rogue follows semantic versioning at the specification level.

---

## Schema Versions

- **Patch updates (X.Y.Z → X.Y.Z+1):**
  - Clarifications
  - Non‑behavioral documentation changes
  - Stricter validation without breaking valid data

- **Minor updates (X.Y → X.Y+1):**
  - Backward‑compatible schema extensions
  - Optional fields with defaults
  - Additive evaluator interfaces

- **Major updates (X → X+1):**
  - Breaking schema changes
  - Changed semantics or invariants
  - Removal of previously valid structures

Major changes require a new schema version and clear migration guidance.

---

## Releases

Tagged releases represent immutable specification snapshots. Consumers should pin to explicit versions.

Unreleased `main` is considered unstable.

