# Security

Binary‑Rogue publishes derived artifacts intended for public consumption.

## Secrets

- Secrets must never be written into artifacts.
- Secrets must be provided via environment variables or secret stores.

## Artifact Safety

Artifacts should be treated as public. Do not embed:

- API keys
- internal hostnames
- private identifiers
- raw ingestion payloads containing headers or tokens

## Prompt and Context Safety

If any evaluator uses prompts or contextual data:

- never log raw prompts that contain secrets
- redact tokens and headers
- store only hashes if persistence is required

## Dependency Hygiene

- Pin dependencies where practical.
- Monitor for known vulnerabilities.
- Run processes with least privilege.

## Network Hygiene

- Restrict outbound network access to required destinations.
- Restrict inbound access to the web server ports only.
