# Changelog

All notable changes to the Binary‑Rogue specification will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-01-18

### Initial Release

Binary‑Rogue v1.0 specification establishing the canonical architecture, semantics, and contracts for a deterministic signal evaluation and story‑prioritization system.

#### Architecture

- Three‑layer architecture (Ingestion → Evaluators → Outputs)
- Deterministic, side‑effect free evaluation model
- Static artifact generation
- Explicit authority boundaries between layers

#### Core Components

- **Ingestion Layer:** Adapter pattern for external signal acquisition
- **Evaluator Layer:** Composable intelligence building blocks
- **Output Layer:** Static JSON artifacts with defined schema

#### Documentation

- System overview and execution model (OVERVIEW.md)
- Complete architectural specification (ARCHITECTURE.md)
- Build lifecycle and phases (BUILD.md)
- Data and intelligence semantics (DATA_INTELLIGENCE.md)
- Evaluator specifications (EVALUATORS.md)
- Output artifact contracts (OUTPUTS.md)
- Frontend rendering requirements (FRONTEND.md)
- Ingestion adapter contracts (INGESTION.md)
- Optional persistence schema (PERSISTENCE.md)
- Operational guidelines (OPERATIONS.md)
- Security constraints (SECURITY.md)
- Versioning policy (VERSIONING.md)
- Reference runtime model (REFERENCE_RUNTIME.md)

#### Schema

- JSON Schema v2020‑12 for `headlines.json` artifacts
- Three lanes: `signal`, `wire`, `flash`
- Three ticker buckets: `tech`, `crypto`, `markets`
- Sentiment scoring: symmetric −2 to +2 range
- Required metadata: schema version, timestamp, build ID

#### Tooling

- Automated validation script (validate_docs.py)
- GitHub Actions CI/CD workflow
- Forbidden phrase detection
- Structural consistency checks

#### Design Principles

- Determinism over real‑time adaptation
- Explainability over black‑box intelligence
- Static outputs over dynamic personalization
- Explicit behavior over autonomous agents
- Auditability over operational complexity

---

## Format Guidelines

### Version Number Format

- **Major.Minor.Patch** (e.g., 1.0.0)
- See VERSIONING.md for semantic versioning policy

### Change Categories

- **Added:** New features or documentation
- **Changed:** Changes to existing functionality
- **Deprecated:** Features to be removed in future versions
- **Removed:** Features removed in this version
- **Fixed:** Bug fixes or corrections
- **Security:** Security‑related changes

### Breaking Changes

Breaking changes are clearly marked with:
- **BREAKING:** prefix in the change description
- Migration guide when applicable
- Justification for the breaking change

---

## Unreleased

### Planned Improvements

Future enhancements under consideration:
- Additional example payloads
- Performance benchmarking guidelines
- Extended test specifications
- Enhanced validation tooling
