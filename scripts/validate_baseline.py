#!/usr/bin/env python3
"""Check the initial EPI baseline. This is a documentation check, not software verification."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = json.loads((ROOT / "baseline.json").read_text(encoding="utf-8"))
DOCS = ROOT / "docs"
ERRORS = []


def check(condition, message):
    if not condition:
        ERRORS.append(message)


def seq(prefix, first, last, digits):
    return [f"{prefix}{i:0{digits}d}" for i in range(first, last + 1)]


expected = {
    "functional": (seq("FR-", 1, 38, 3), "REQUIREMENTS_REGISTER.md"),
    "nonfunctional": (seq("NFR-", 1, 11, 3), "REQUIREMENTS_REGISTER.md"),
    "decisions": (seq("ADR-P", 1, 9, 2), "ARCHITECTURE_DECISIONS.md"),
    "scenarios": (seq("SC-", 1, 12, 2), "VERIFICATION_STRATEGY.md"),
    "milestones": (seq("M", 0, 23, 2), "IMPLEMENTATION_ROADMAP.md"),
    "crosswalk": (seq("INIT.MH-", 1, 14, 2) + seq("D02.BASE-", 1, 5, 2) + seq("D02.EXT-", 1, 3, 2) + seq("D03.DOM-", 1, 12, 2), "REQUIREMENTS_REGISTER.md"),
    "moneyhub": (seq("D02.MH-", 1, 9, 2), "REQUIREMENTS_REGISTER.md"),
    "unknowns": (seq("U-", 1, 7, 2), "RESEARCH_ASSUMPTIONS_EVIDENCE.md"),
}

check(BASE["version"] == "0.1.0", "Unexpected initial baseline version")
check([item["id"] for item in BASE["source_documents"]] == ["D01", "D02", "D03", "D04"], "Source manifest must contain the four approved PDFs")
for item in BASE["source_documents"]:
    p = ROOT / item["file"]
    check(p.is_file(), f"Missing source: {p}")
    if p.is_file():
        check(hashlib.sha256(p.read_bytes()).hexdigest() == item["sha256"], f"Source fingerprint mismatch: {p}")

for name, (ids, filename) in expected.items():
    items = BASE["catalogues"][name]
    check([item["id"] for item in items] == ids, f"{name}: unexpected or missing identifier")
    text = (DOCS / filename).read_text(encoding="utf-8")
    for item in items:
        marker = "### " + item["id"] + "\n\n"
        check(text.count(marker) == 1, f"{item['id']}: missing or duplicated heading in {filename}")
        check(marker + item["text"] in text, f"{item['id']}: catalogue wording differs from baseline")
    print(f"{name}: {len(items)} baseline entries checked")

req = (DOCS / "REQUIREMENTS_REGISTER.md").read_text(encoding="utf-8")
for item in BASE["source_definitions"]["document_02"]:
    check(item["text"] in req, f"Missing original definition: {item['id']}")
for item in BASE["source_definitions"]["document_03"]:
    check(item["text"] + " Acceptance evidence: " + item["acceptance"] in req, f"Missing original definition: {item['id']}")

for p in ROOT.rglob("*.md"):
    text = p.read_text(encoding="utf-8")
    check("\u2014" not in text, f"Em dash in {p.name}")
    check(not re.search(r"(?m)^\s*\|", text), f"Table row in {p.name}")
    for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if not link.startswith(("http:", "https:", "#")):
            check((p.parent / link.split("#")[0]).exists(), f"Broken local link in {p.name}: {link}")

if ERRORS:
    print("FAILED documentation baseline checks:", file=sys.stderr)
    for error in ERRORS:
        print("- " + error, file=sys.stderr)
    sys.exit(1)
print("PASS: source fingerprints, canonical IDs, catalogue text, source definitions, Markdown format and local links.")
print("No engineering, infrastructure, payment or regulatory verification was performed.")
