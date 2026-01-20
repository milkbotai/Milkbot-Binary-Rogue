# Validation Checklist (v1.0)

Use this checklist before publishing or releasing updates.

---

## Automated Validation

Run the comprehensive validation script:

```bash
python3 tools/validate_docs.py
```

Expected output: `OK`

Review the detailed report:
```bash
cat tools/validation_report.json
```

### Validation Checks Performed

The automated validation performs these checks:

1. **File Existence** – All required files present
2. **Forbidden Phrases** – No work-in-progress markers (TODO, TBD, FIXME)
3. **Required Content** – Color palette, VPS IP, lanes, ticker buckets
4. **Schema Validation** – JSON schema is structurally valid
5. **Internal Links** – All markdown links point to existing files
6. **JSON Examples** – All JSON code blocks in docs are valid
7. **Example Payloads** – All example files validate against schema

---

## Manual Checklist

### Structural Requirements

- [ ] All required files exist
  - [ ] `README.md` (entry point)
  - [ ] `LICENSE` (Apache‑2.0)
  - [ ] `NOTICE` (attribution)
  - [ ] `CONTRIBUTING.md` (contribution guide)
  - [ ] `CHANGELOG.md` (version history)
  - [ ] `VALIDATION.md` (this file)
  - [ ] All 14 docs in `docs/`
  - [ ] Schema in `schemas/headlines.schema.json`
  - [ ] Examples in `examples/`

### Semantic Consistency

- [ ] No work-in-progress markers in spec docs
- [ ] Terminology is consistent across all documents
- [ ] No contradictory statements
- [ ] Ingestion layer is transport‑agnostic
- [ ] Frontend contract includes palette and performance constraints
- [ ] All core concepts defined in DATA_INTELLIGENCE.md

### Contract Consistency

- [ ] `docs/OUTPUTS.md` matches `schemas/headlines.schema.json`
- [ ] Lanes are `signal|wire|flash` everywhere
- [ ] Ticker buckets are `tech|crypto|markets` everywhere
- [ ] Sentiment range is −2 to +2 consistently
- [ ] Schema version is "1.0" consistently
- [ ] Build phases match across BUILD.md and OVERVIEW.md

### Content Verification

- [ ] `docs/FRONTEND.md` specifies `#0a0a0a` background
- [ ] `docs/OPERATIONS.md` includes VPS IP `86.48.24.74`
- [ ] `docs/OVERVIEW.md` includes complete documentation roadmap
- [ ] `docs/BUILD.md` includes performance benchmarks
- [ ] `docs/OPERATIONS.md` includes deployment procedures
- [ ] `docs/TESTING.md` specifies test requirements

### Examples and Test Cases

- [ ] Example payloads validate against schema
- [ ] Signal examples show realistic input structure
- [ ] Test cases cover key scenarios (determinism, schema compliance)
- [ ] All JSON examples in markdown are syntactically valid

### Code Quality

- [ ] Validation script runs without errors
- [ ] Schema is valid JSON and valid JSON Schema
- [ ] No syntax errors in any files
- [ ] Internal links all resolve correctly

---

## Pre‑Release Verification

Before tagging a release:

1. **Run full validation**
   ```bash
   python3 tools/validate_docs.py
   ```

2. **Verify all files committed**
   ```bash
   git status
   # Should show clean working tree
   ```

3. **Test example payloads**
   ```bash
   # If jsonschema is installed:
   jsonschema -i examples/payloads/complete.json schemas/headlines.schema.json
   jsonschema -i examples/payloads/minimal.json schemas/headlines.schema.json
   ```

4. **Check documentation completeness**
   - Read through OVERVIEW.md roadmap
   - Verify all referenced documents exist
   - Check for broken links (validation checks this)

5. **Verify version consistency**
   - `CHANGELOG.md` has current version
   - Schema version matches
   - No "unreleased" content in CHANGELOG

---

## CI/CD Integration

GitHub Actions automatically runs validation on:
- Every push
- Every pull request

Workflow location: `.github/workflows/validate.yml`

The workflow must pass before merging to main.

---

## Troubleshooting Validation Failures

### Missing Files
```
Error: Missing files: docs/TESTING.md
```
**Fix:** Create the missing file or verify it's in the correct location.

### Forbidden Phrases
```
Error: Forbidden phrases: docs/BUILD.md: TODO
```
**Fix:** Remove work-in-progress markers. Complete or remove incomplete sections.

### Broken Internal Links
```
Error: Broken internal links: README.md → docs/MISSING.md
```
**Fix:** Update the link to point to an existing file or create the referenced file.

### Invalid JSON Examples
```
Error: Invalid JSON in docs/OUTPUTS.md (example #2)
```
**Fix:** Correct the JSON syntax in the code block.

### Schema Validation Failure
```
Error: examples/payloads/test.json fails schema validation
```
**Fix:** Update the example payload to match the schema requirements.

---

## Validation Report Structure

The `validation_report.json` contains:

```json
{
  "ok": true/false,
  "missing_files": [],
  "forbidden_hits": [],
  "required_checks": {},
  "schema": {},
  "internal_links": {},
  "json_examples": {},
  "example_payloads": {}
}
```

Each section provides detailed information about what passed or failed.

---

## Continuous Validation

For active development:

```bash
# Watch for changes and re-validate
watch -n 5 python3 tools/validate_docs.py
```

---

This validation ensures Binary‑Rogue maintains specification quality and consistency.
