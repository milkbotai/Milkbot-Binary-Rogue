# Output Artifacts

Binary‑Rogue emits static artifacts intended for read‑only consumption.

Artifacts are presentation views, not systems of record.

## Artifact Principles

- Self‑describing metadata: `generated_at`, `schema_version`
- Deterministic ordering and explicit tie‑breakers
- Backward‑compatible evolution when structure changes
- Atomic writes (consumers must not see partial output)

## Primary Artifact: Headlines Payload (JSON)

The primary artifact is a single JSON document consumed by the frontend.

### Frontend Coupling Rules

- The frontend fetches **one payload** at load.
- No supplementary network requests are permitted for render.
- Rendering must be deterministic for identical input.

### Canonical Shape (v1.0)

- `lanes.signal|wire|flash` are the three headline lanes.
- `ticker.tech|crypto|markets` backs the market strip.

Example (illustrative):

```json
{
  "meta": {
    "schema_version": "1.0.0",
    "generated_at": "2026-01-18T00:00:00Z",
    "build_id": "opaque"
  },
  "alert": {
    "headline": "EXAMPLE ALERT",
    "url": "https://example.com",
    "source": "Example",
    "published": "2026-01-18T00:00:00Z",
    "sentiment": 0,
    "cluster_size": 3
  },
  "lanes": {
    "signal": [],
    "wire": [],
    "flash": []
  },
  "ticker": {
    "tech": [],
    "crypto": [],
    "markets": []
  }
}
```

### Versioning

`schema_version` is required. Breaking changes increment the major version.
