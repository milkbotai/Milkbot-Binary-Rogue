# Testing Specifications

Binary‑Rogue implementations must verify deterministic behavior, schema compliance, and evaluator correctness.

---

## Testing Categories

### 1. Determinism Tests

**Requirement:** Identical inputs must produce identical outputs.

#### Test Procedure

```python
def test_determinism():
    """
    Run build twice with identical inputs.
    Outputs must be byte-for-byte identical.
    """
    signals = load_test_signals("test-set-001.json")
    
    # Run 1
    output_1 = run_build(signals, build_id="determinism-test")
    
    # Run 2 (same inputs)
    output_2 = run_build(signals, build_id="determinism-test")
    
    # Compare
    assert output_1 == output_2, "Outputs must be identical"
```

#### Acceptable Differences

The only acceptable difference is `meta.generated_at` if using system timestamps. All other fields must be identical.

To ensure full determinism, either:
- Use a fixed timestamp in test mode
- Exclude `meta.generated_at` from comparison
- Use a seeded timestamp generator

---

### 2. Schema Validation Tests

**Requirement:** All output artifacts must validate against `schemas/headlines.schema.json`.

#### Test Procedure

```python
import json
import jsonschema

def test_schema_compliance():
    """
    Validate output artifact against schema.
    """
    schema = json.load(open("schemas/headlines.schema.json"))
    output = run_build(test_signals)
    
    # This will raise if invalid
    jsonschema.validate(output, schema)
```

#### Required Validations

- All required fields present
- All field types correct
- Sentiment values in range [−2, 2]
- Weight values ≥ 0
- Cluster sizes ≥ 1
- Timestamps in ISO 8601 format
- URLs are valid strings
- No additional properties where `additionalProperties: false`

#### Edge Cases

Test these specific scenarios:
- Empty lanes (all arrays empty)
- Null alert (no breaking story)
- Empty ticker buckets
- Maximum sentiment (+2, −2)
- Zero weight stories
- Single cluster (cluster_size = 1)

---

### 3. Evaluator Unit Tests

**Requirement:** Each evaluator must have isolated unit tests.

#### Test Structure

```python
def test_sentiment_evaluator():
    """
    Test sentiment scoring in isolation.
    """
    evaluator = SentimentEvaluator()
    
    # Positive signal
    signal_positive = Signal(
        headline="Breakthrough in cancer research",
        text="Major advancement in treatment..."
    )
    score = evaluator.evaluate(signal_positive)
    assert score > 0, "Positive signal must have positive sentiment"
    
    # Negative signal
    signal_negative = Signal(
        headline="Security breach exposes user data",
        text="Millions of accounts compromised..."
    )
    score = evaluator.evaluate(signal_negative)
    assert score < 0, "Negative signal must have negative sentiment"
    
    # Neutral signal
    signal_neutral = Signal(
        headline="Company announces quarterly results",
        text="Revenue meets expectations..."
    )
    score = evaluator.evaluate(signal_neutral)
    assert -1 <= score <= 1, "Neutral signal should have mild sentiment"
```

#### Required Tests Per Evaluator

1. **Input validation** – Handles malformed inputs gracefully
2. **Output range** – Returns values in expected range
3. **Edge cases** – Empty strings, very long text, special characters
4. **Determinism** – Same input always produces same output
5. **No side effects** – Does not modify input or external state

---

### 4. Integration Tests

**Requirement:** Complete build pipeline from signals to artifacts.

#### Test Procedure

```python
def test_full_pipeline():
    """
    End-to-end test: signals → build → artifact
    """
    # Acquire signals
    signals = ingest_from_test_source()
    
    # Run build
    artifact = run_build(signals)
    
    # Verify structure
    assert "meta" in artifact
    assert "lanes" in artifact
    assert "ticker" in artifact
    
    # Verify content quality
    assert len(artifact["lanes"]["signal"]) > 0, "Should have signal stories"
    
    # Verify ordering
    weights = [s["weight"] for s in artifact["lanes"]["signal"]]
    assert weights == sorted(weights, reverse=True), "Stories must be ordered by weight"
```

#### Integration Scenarios

- **Full build** – All phases execute successfully
- **Empty input** – Handles zero signals gracefully
- **High volume** – 1000+ signals process correctly
- **Mixed sources** – Multiple adapters produce consistent results
- **Alert selection** – Top story correctly promoted to alert

---

### 5. Performance Tests

**Requirement:** Build completes within acceptable time constraints.

#### Target Performance

| Phase | Target Time | Maximum Time |
|-------|-------------|--------------|
| Ingestion | < 10 seconds | 30 seconds |
| Evaluation | < 30 seconds | 60 seconds |
| Output generation | < 5 seconds | 15 seconds |
| **Total build** | **< 45 seconds** | **90 seconds** |

#### Test Procedure

```python
import time

def test_build_performance():
    """
    Verify build completes within time constraints.
    """
    signals = generate_test_signals(count=500)
    
    start = time.time()
    artifact = run_build(signals)
    duration = time.time() - start
    
    assert duration < 45.0, f"Build took {duration}s, target is 45s"
```

#### Performance Scenarios

- **Typical load** – 100 signals, < 10 seconds
- **High load** – 1000 signals, < 45 seconds
- **Stress test** – 5000 signals, < 90 seconds

---

### 6. Error Handling Tests

**Requirement:** System handles failures gracefully.

#### Test Scenarios

```python
def test_malformed_signal():
    """
    Handle signals with missing fields.
    """
    malformed = {"headline": "Test"}  # Missing required fields
    result = process_signal(malformed)
    
    # Should log error and skip, not crash
    assert result is None or result.is_error()

def test_evaluator_failure():
    """
    Handle evaluator exceptions.
    """
    signal = create_test_signal()
    
    with mock.patch('evaluator.process', side_effect=Exception("API timeout")):
        # Build should complete, possibly with reduced confidence
        artifact = run_build([signal])
        assert artifact is not None
```

#### Required Error Handling

- Malformed signals skipped with logging
- Evaluator failures reduce confidence, don't crash build
- Network timeouts have exponential backoff
- Invalid schema outputs rejected before write
- Duplicate signals deduplicated

---

### 7. Regression Tests

**Requirement:** Changes don't break existing behavior.

#### Test Procedure

Maintain a golden dataset:
- Known input signals
- Expected output artifacts
- Run on every change

```python
def test_regression_golden_dataset():
    """
    Verify outputs match known-good results.
    """
    signals = load_golden_signals()
    artifact = run_build(signals, build_id="golden-001")
    
    expected = load_golden_artifact()
    
    # Compare (excluding timestamp)
    assert_artifacts_equivalent(artifact, expected)
```

---

## Test Data

### Test Signal Sets

Maintain diverse test datasets:

1. **Minimal** – 5 signals, basic coverage
2. **Typical** – 100 signals, realistic distribution
3. **Large** – 1000 signals, stress test
4. **Edge cases** – Unusual content, special characters, long text
5. **Golden** – Known-good dataset for regression

### Test Data Location

```
examples/
└── test-cases/
    ├── minimal-signals.json
    ├── typical-signals.json
    ├── large-signals.json
    ├── edge-cases.json
    └── golden-dataset/
```

---

## Continuous Integration

### Required CI Checks

Every pull request must pass:

1. ✅ All unit tests
2. ✅ Schema validation
3. ✅ Determinism verification
4. ✅ Performance benchmarks (warning if slow, fail if > 2x target)
5. ✅ Integration tests
6. ✅ Regression tests

### CI Configuration

```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install jsonschema pytest pytest-benchmark
      
      - name: Run unit tests
        run: pytest tests/unit/
      
      - name: Run integration tests
        run: pytest tests/integration/
      
      - name: Validate schema compliance
        run: pytest tests/schema/
      
      - name: Performance benchmarks
        run: pytest tests/performance/ --benchmark-only
```

---

## Test Coverage Requirements

### Minimum Coverage

- **Unit tests:** 80% code coverage
- **Integration tests:** All critical paths
- **Schema validation:** 100% of output artifacts
- **Determinism:** All evaluators verified

### Coverage Reporting

```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html
```

---

## Manual Testing

### Pre‑Release Checklist

Before any release:

- [ ] All automated tests pass
- [ ] Manual smoke test with real data sources
- [ ] Visual inspection of output artifact
- [ ] Frontend rendering verification
- [ ] Performance profiling completed
- [ ] Error logs reviewed for anomalies
- [ ] Documentation updated if needed

---

## Test Automation Tools

### Recommended Tools

- **pytest** – Test framework
- **jsonschema** – Schema validation
- **hypothesis** – Property-based testing
- **pytest-benchmark** – Performance testing
- **coverage.py** – Code coverage

### Example Test Setup

```python
# tests/conftest.py
import pytest

@pytest.fixture
def test_signals():
    """Provide standard test signal set."""
    return load_signals("examples/test-cases/typical-signals.json")

@pytest.fixture
def schema():
    """Provide schema for validation."""
    return load_schema("schemas/headlines.schema.json")
```

---

## Testing Best Practices

1. **Isolate tests** – No shared state between tests
2. **Use fixtures** – Reusable test data and setup
3. **Test one thing** – Each test verifies one behavior
4. **Descriptive names** – Test names explain what's tested
5. **Fast tests** – Unit tests run in milliseconds
6. **Deterministic tests** – No random failures
7. **Clear assertions** – Failure messages are helpful

---

## Failure Investigation

When tests fail:

1. Check test output for specific assertion
2. Review logs for errors or warnings
3. Reproduce locally with same inputs
4. Use debugger to step through code
5. Verify test assumptions are still valid
6. Check for environmental differences

---

## Future Testing Improvements

Potential enhancements:

- Property‑based testing with hypothesis
- Fuzzing for edge case discovery
- Load testing with production‑scale data
- Security testing for input validation
- Mutation testing for test quality

---

This testing specification ensures Binary‑Rogue implementations are correct, reliable, and performant.
