# Examples

This directory contains reference examples for Binary‑Rogue implementations.

---

## Directory Structure

```
examples/
├── payloads/         Complete output artifact examples
├── signals/          Raw signal input examples
└── test-cases/       Validation and test scenarios
```

---

## Usage

### Payload Examples

Complete, valid output artifacts demonstrating the schema structure.

Use these to:
- Understand the complete artifact format
- Validate your implementation outputs
- Test frontend rendering
- Verify schema compliance

### Signal Examples

Raw signal inputs before normalization and evaluation.

Use these to:
- Understand ingestion adapter outputs
- Test signal normalization logic
- Validate evaluator inputs

### Test Cases

Specific scenarios for validation and testing.

Use these to:
- Verify deterministic behavior
- Test edge cases
- Validate error handling
- Ensure schema compliance

---

## Schema Compliance

All payload examples are validated against `schemas/headlines.schema.json`.

To validate an example:

```bash
# Using Python with jsonschema
pip install jsonschema
python3 -c "
import json
import jsonschema
schema = json.load(open('schemas/headlines.schema.json'))
payload = json.load(open('examples/payloads/basic.json'))
jsonschema.validate(payload, schema)
print('Valid!')
"
```

---

## Contributing Examples

When adding new examples:

1. Ensure schema compliance
2. Use realistic, representative data
3. Include clear descriptions
4. Follow naming conventions
5. Update this README

See CONTRIBUTING.md for complete guidelines.
