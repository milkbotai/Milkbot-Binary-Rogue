# Contributing to Binary‑Rogue

Binary‑Rogue is a specification repository. Contributions should focus on clarifying, extending, or correcting the specification itself.

---

## Types of Contributions

### Specification Improvements

- Clarifying ambiguous language
- Adding missing semantic definitions
- Correcting technical inaccuracies
- Improving examples and illustrations
- Enhancing schema definitions

### Documentation Enhancements

- Fixing typos or grammatical errors
- Improving document structure
- Adding cross‑references
- Updating diagrams or visualizations

### Tooling Improvements

- Enhancing validation scripts
- Adding new validation checks
- Improving CI/CD workflows
- Creating helpful utilities

---

## Contribution Process

### 1. Check Existing Issues

Before starting work, check if an issue already exists for your proposed change.

### 2. Open an Issue First

For significant changes, open an issue describing:
- What you want to change
- Why the change is needed
- How it improves the specification

### 3. Fork and Branch

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Binary-Rogue.git
cd Binary-Rogue

# Create a feature branch
git checkout -b feature/your-feature-name
```

### 4. Make Changes

Follow these guidelines:
- Maintain consistency with existing terminology
- Update all affected documents
- Run validation before committing
- Keep changes focused and atomic

### 5. Validate Your Changes

```bash
# Run the validation script
python3 tools/validate_docs.py

# Ensure it outputs: OK
```

### 6. Commit with Clear Messages

```bash
git add .
git commit -m "Brief description of change

Detailed explanation of what changed and why."
```

### 7. Submit a Pull Request

- Reference any related issues
- Describe what changed
- Explain the rationale
- Ensure CI checks pass

---

## Style Guidelines

### Markdown Formatting

- Use ATX‑style headers (`#`, `##`, `###`)
- Use fenced code blocks with language identifiers
- Use consistent list formatting (dashes for unordered, numbers for ordered)
- Maintain proper spacing (blank lines between sections)

### Terminology Consistency

Binary‑Rogue has specific semantic terms. When contributing:

- Use "signal" (not "event" or "message")
- Use "story" (not "article" or "content")
- Use "evaluator" (not "processor" or "analyzer")
- Use "lane" (not "category" or "section")
- Use "artifact" (not "output" or "file")

See `docs/DATA_INTELLIGENCE.md` for complete terminology.

### Code Examples

When adding code examples:
- Use realistic, representative data
- Include comments for clarity
- Ensure examples are syntactically valid
- Match the schema specifications

### Schema Changes

Schema changes require:
- Backward compatibility justification
- Updated examples in `examples/`
- Updated OUTPUTS.md documentation
- Versioning consideration (see VERSIONING.md)

---

## Validation Requirements

All contributions must pass:

### Automated Checks

- File existence validation
- Forbidden phrase detection
- Required element validation
- Schema structural validation
- JSON syntax validation
- Markdown formatting checks

### Manual Review

- Semantic consistency across documents
- Clarity and readability
- Alignment with core principles
- Completeness of examples

---

## Forbidden Content

Do not include:

- Phrases like "TODO", "TBD", "FIXME"
- References to "old", "previous", "revised"
- External service dependencies without justification
- Implementation‑specific runtime details
- Non‑deterministic behavior descriptions

---

## Semantic Versioning

Binary‑Rogue follows semantic versioning at the specification level:

- **Patch (1.0.x):** Typo fixes, clarifications, non‑semantic changes
- **Minor (1.x.0):** Backward‑compatible additions
- **Major (x.0.0):** Breaking changes requiring coordination

See `docs/VERSIONING.md` for complete policy.

---

## Review Process

1. **Automated validation** runs on all pull requests
2. **Maintainer review** ensures consistency and quality
3. **Discussion** may request changes or clarifications
4. **Approval** merges the contribution

---

## Getting Help

- Open an issue for questions
- Reference existing documentation
- Ask for clarification on terminology
- Request feedback on proposed changes

---

## License

By contributing to Binary‑Rogue, you agree that your contributions will be licensed under the Apache License 2.0.

All contributions must include appropriate copyright notices and comply with the license terms defined in the LICENSE file.

---

## Recognition

Contributors are recognized in release notes and may be mentioned in project documentation where appropriate.

Thank you for helping improve Binary‑Rogue!
