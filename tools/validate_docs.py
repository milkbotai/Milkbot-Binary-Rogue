import json
import os
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DOCS = BASE / "docs"
SCHEMAS = BASE / "schemas"
EXAMPLES = BASE / "examples"

REQUIRED_FILES = [
  BASE / "README.md",
  BASE / "LICENSE",
  BASE / "NOTICE",
  BASE / "VALIDATION.md",
  BASE / "CONTRIBUTING.md",
  BASE / "CHANGELOG.md",
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
  DOCS / "TESTING.md",
  DOCS / "VERSIONING.md",
  SCHEMAS / "headlines.schema.json",
]

FORBIDDEN = [
  r"\bTODO\b",
  r"\bTBD\b",
  r"\bFIXME\b",
  r"\bXXX\b",
  r"\bHACK\b",
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
  "internal_links": {},
  "json_examples": {},
  "example_payloads": {},
}

# 1) Required files
for f in REQUIRED_FILES:
  if not f.exists():
    REPORT["ok"] = False
    REPORT["missing_files"].append(str(f.relative_to(BASE)))

# 2) Forbidden phrases (skip CONTRIBUTING.md and VALIDATION.md as they document forbidden patterns)
for path in list([BASE / "README.md", BASE / "NOTICE", BASE / "CHANGELOG.md"]) + list(DOCS.glob("*.md")):
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

# 5) Internal link validation
md_files = list(DOCS.glob("*.md")) + [BASE / "README.md", BASE / "CONTRIBUTING.md", BASE / "CHANGELOG.md"]
link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')
broken_links = []

for md_file in md_files:
  if not md_file.exists():
    continue
  text = md_file.read_text(encoding="utf-8", errors="replace")
  matches = link_pattern.findall(text)
  
  for link_text, link_path in matches:
    if link_path.startswith('docs/'):
      target = BASE / link_path
    elif link_path.startswith('../'):
      target = (md_file.parent / link_path).resolve()
    else:
      target = (md_file.parent / link_path).resolve()
    
    if not target.exists():
      broken_links.append({
        "file": str(md_file.relative_to(BASE)),
        "link_text": link_text,
        "target": link_path,
        "resolved": str(target)
      })

REPORT["internal_links"] = {
  "ok": len(broken_links) == 0,
  "broken_count": len(broken_links),
  "broken_links": broken_links
}
if broken_links:
  REPORT["ok"] = False

# 6) Validate JSON examples in markdown
json_example_pattern = re.compile(r'```json\s*\n(.*?)\n```', re.DOTALL)
json_errors = []

for md_file in md_files:
  if not md_file.exists():
    continue
  text = md_file.read_text(encoding="utf-8", errors="replace")
  matches = json_example_pattern.findall(text)
  
  for i, json_text in enumerate(matches):
    try:
      json.loads(json_text)
    except json.JSONDecodeError as e:
      json_errors.append({
        "file": str(md_file.relative_to(BASE)),
        "example_number": i + 1,
        "error": str(e)
      })

REPORT["json_examples"] = {
  "ok": len(json_errors) == 0,
  "error_count": len(json_errors),
  "errors": json_errors
}
if json_errors:
  REPORT["ok"] = False

# 7) Validate example payloads against schema
if (EXAMPLES / "payloads").exists() and schema_path.exists():
  try:
    import jsonschema
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    payload_validation = []
    
    for payload_file in (EXAMPLES / "payloads").glob("*.json"):
      try:
        payload = json.loads(payload_file.read_text(encoding="utf-8"))
        jsonschema.validate(payload, schema)
        payload_validation.append({
          "file": str(payload_file.relative_to(BASE)),
          "valid": True
        })
      except jsonschema.ValidationError as e:
        payload_validation.append({
          "file": str(payload_file.relative_to(BASE)),
          "valid": False,
          "error": str(e.message)
        })
        REPORT["ok"] = False
      except Exception as e:
        payload_validation.append({
          "file": str(payload_file.relative_to(BASE)),
          "valid": False,
          "error": str(e)
        })
        REPORT["ok"] = False
    
    REPORT["example_payloads"] = {
      "ok": all(p["valid"] for p in payload_validation),
      "count": len(payload_validation),
      "payloads": payload_validation
    }
  except ImportError:
    REPORT["example_payloads"] = {
      "ok": None,
      "note": "jsonschema not installed, skipping payload validation"
    }
else:
  REPORT["example_payloads"] = {
    "ok": None,
    "note": "No example payloads or schema not found"
  }

out_path = BASE / "tools" / "validation_report.json"
out_path.write_text(json.dumps(REPORT, indent=2), encoding="utf-8")

print("OK" if REPORT["ok"] else "FAIL")

if not REPORT["ok"]:
  if REPORT["missing_files"]:
    print(f"\nMissing files: {len(REPORT['missing_files'])}")
    for f in REPORT["missing_files"]:
      print(f"  - {f}")
  
  if REPORT["forbidden_hits"]:
    print(f"\nForbidden phrases: {len(REPORT['forbidden_hits'])}")
    for hit in REPORT["forbidden_hits"]:
      print(f"  - {hit['file']}: {hit['pattern']}")
  
  if not REPORT["required_checks"].get("ok", True):
    print("\nRequired checks failed:")
    for name, check in REPORT["required_checks"].items():
      if not check.get("ok"):
        print(f"  - {name}: {check}")
  
  if not REPORT["internal_links"]["ok"]:
    print(f"\nBroken internal links: {REPORT['internal_links']['broken_count']}")
    for link in REPORT["internal_links"]["broken_links"]:
      print(f"  - {link['file']}: [{link['link_text']}]({link['target']})")
  
  if not REPORT["json_examples"]["ok"]:
    print(f"\nInvalid JSON examples: {REPORT['json_examples']['error_count']}")
    for err in REPORT["json_examples"]["errors"]:
      print(f"  - {err['file']} (example #{err['example_number']}): {err['error']}")
  
  if REPORT["example_payloads"].get("ok") is False:
    print("\nInvalid example payloads:")
    for p in REPORT["example_payloads"]["payloads"]:
      if not p["valid"]:
        print(f"  - {p['file']}: {p['error']}")
