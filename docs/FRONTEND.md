# Frontend Contract (Looks + Speed)

This document defines the canonical layout, visual rules, and rendering constraints for the Binary‑Rogue static frontend.

The frontend is a deterministic renderer of a single artifact:

- One payload is fetched at load.
- No background activity after first render.
- No supplementary network requests are permitted.

## Visual Constraints

The frontend is intentionally austere and text‑dominant.

### Non‑Negotiable Rules

- Page background is `#0a0a0a`.
- Primary text is solid white; secondary text is muted gray.
- No cards, containers, shadows, gradients, or rounded elements.
- No thumbnails, images, or embedded media.
- All visual structure is achieved through spacing, typography, and thin rules only.

## Color System (Fixed Tokens)

These values must not drift without an explicit specification change:

- `--bg`: `#0a0a0a` — background
- `--fg`: `#ffffff` — primary text
- `--muted`: `#b7b7b7` — secondary text
- `--steel`: `#2a2f36` — standard divider rules
- `--steel-strong`: `#3a414a` — top‑zone separator

## Page Structure

### Top Zone

Full width, above the lanes:

1. Masthead: “Binary Rogue”
2. Tagline: “Glitch the System. Burn the Map.”
3. Market strip (ticker)
4. ALERT block

### ALERT Block

- Displays the highest‑ranked story.
- Dominant via size/weight only.
- Strictly text‑based.

## Lanes

### Desktop

- Three lanes: `SIGNAL`, `WIRE`, `FLASH`
- Up to twenty items per lane
- Thin vertical divider rules

### Mobile

- Single‑column stack order: SIGNAL → WIRE → FLASH
- Up to ten items per section initially
- Remaining items revealed via inline expand control

## Typography

- System UI font stack only (no external font loading).
- Underlines appear only on hover or keyboard focus.
- All interactive elements must display a visible focus outline.

## Data Binding

The frontend renders from one payload (`/headlines.json`). Mapping:

- `alert` → ALERT block
- `lanes.signal[]` → SIGNAL lane
- `lanes.wire[]` → WIRE lane
- `lanes.flash[]` → FLASH lane
- `ticker.tech|crypto|markets` → Market strip

No cross‑lane inference or reordering occurs in the client.

## Performance Requirements

- Initial render must complete quickly on low‑end devices.
- JavaScript must be minimal and framework‑free.
- CSS must be a single file or inline; no external dependencies.
