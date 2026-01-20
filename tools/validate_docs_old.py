import json
import os
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DOCS = BASE / "docs"
SCHEMAS = BASE / "schemas"

REQUIRED_FILES = [
  BASE / "README.md",
  BASE / "LICENSE",
  BASE / "NOTICE",
  BASE / "VALIDATION.md",
  DOCS / "OVERVIEW.md",
  DOCS / "ARCHITECTURE.md",
  DOCS / "BUILD.md",
  DOCS / "DATA_INTELLIGENCE.md",
  DOCS / "EVALUATORS.md",
  DOCS / "FRONTEND.md",
  DOCS / "INGESTION.md",
  DOCS / "OPERATIONS.md",
  DOCS / "OUTPUTS.md",
  DOCS / "PERSISTENCE.md",
  DOCS / "REFERENCE_RUNTIME.md",
  DOCS / "SECURITY.md",
  DOCS / "VERSIONING.md",
  SCHEMAS / "headlines.schema.json",
]

FORBIDDEN = [
  r"previous",
  r"old",
  r"outdated",
  r"revised",
  r"changed",
  r"revision",
  r"TODO",
  r"TBD",
  r"RSS",
]

REQUIRED_CHECKS = {
  "frontend_bg": (DOCS / "FRONTEND.md", r"#0a0a0a"),
  "ops_ip": (DOCS / "OPERATIONS.md", r"86\.48\.24\.74"),
  "lanes_and_ticker": (DOCS / "OUTPUTS.md", r"lanes\.signal\|wire\|flash"),
  "ticker_buckets": (DOCS / "OUTPUTS.md", r"ticker\.tech\|crypto\|markets"),
}

REPORT = {
  "ok": True,
  "missing_files": [],
  "forbidden_hits": [],
  "required_checks": {},
  "schema": {},
}

# 1) Required files
for f in REQUIRED_FILES:
  if not f.exists():
    REPORT["ok"] = False
    REPORT["missing_files"].append(str(f.relative_to(BASE)))

# 2) Forbidden phrases
for path in list([BASE / "README.md", BASE / "VALIDATION.md", BASE / "NOTICE"] ) + list(DOCS.glob("*.md")):
  if not path.exists():
    continue
  text = path.read_text(encoding="utf-8", errors="replace")
  for pat in FORBIDDEN:
    if re.search(pat, text, flags=re.IGNORECASE):
      REPORT["ok"] = False
      REPORT["forbidden_hits"].append({"file": str(path.relative_to(BASE)), "pattern": pat})

# 3) Required checks
for name, (path, needle) in REQUIRED_CHECKS.items():
  if not path.exists():
    REPORT["ok"] = False
    REPORT["required_checks"][name] = {"ok": False, "reason": "missing file"}
    continue
  text = path.read_text(encoding="utf-8", errors="replace")
  ok = re.search(needle, text, flags=re.IGNORECASE) is not None
  REPORT["required_checks"][name] = {"ok": ok, "needle": needle, "file": str(path.relative_to(BASE))}
  if not ok:
    REPORT["ok"] = False

# 4) Schema checks
schema_path = SCHEMAS / "headlines.schema.json"
if schema_path.exists():
  try:
    s = json.loads(schema_path.read_text(encoding="utf-8"))
    # Minimal structural expectations
    req = s.get("required", [])
    props = s.get("properties", {})
    lanes = props.get("lanes", {}).get("required", [])
    ticker = props.get("ticker", {}).get("required", [])
    REPORT["schema"] = {
      "ok": True,
      "required": req,
      "lanes_required": lanes,
      "ticker_required": ticker,
    }
    for needed in ["meta", "lanes", "ticker"]:
      if needed not in req:
        REPORT["schema"]["ok"] = False
        REPORT["ok"] = False
    for needed in ["signal", "wire", "flash"]:
      if needed not in lanes:
        REPORT["schema"]["ok"] = False
        REPORT["ok"] = False
    for needed in ["tech", "crypto", "markets"]:
      if needed not in ticker:
        REPORT["schema"]["ok"] = False
        REPORT["ok"] = False
  except Exception as e:
    REPORT["schema"] = {"ok": False, "error": str(e)}
    REPORT["ok"] = False
else:
  REPORT["schema"] = {"ok": False, "error": "missing schema"}
  REPORT["ok"] = False

# Write report
out_path = BASE / "tools" / "validation_report.json"
out_path.write_text(json.dumps(REPORT, indent=2), encoding="utf-8")

# Print summary
print("OK" if REPORT["ok"] else "FAIL")
