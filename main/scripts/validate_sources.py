#!/usr/bin/env python3
"""Source Validator — confirms all sourceRef values resolve to known sources."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "main" / "data"

ERRORS = []

TECHNICAL_PAGE_TYPES = {
    "technical_reference", "constraint_page", "country_profile",
    "program_profile", "source_brief", "claim_review",
}


def error(msg: str):
    ERRORS.append(msg)
    print(f"  [FAIL] {msg}")


def load_json(path: Path) -> dict | None:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        error(f"{path.name}: JSON parse error: {e}")
        return None


def load_known_sources() -> set:
    path = DATA_DIR / "source_claims.json"
    if not path.exists():
        return set()
    data = load_json(path)
    if not data:
        return set()
    return {s["id"] for s in data.get("sources", [])}


def validate_program_sources(known_sources: set):
    path = DATA_DIR / "program_registry.json"
    if not path.exists():
        return
    data = load_json(path)
    if not data:
        return
    for prog in data.get("programs", []):
        pid = prog.get("id", "<no-id>")
        source_refs = prog.get("sourceRef", [])
        if not source_refs:
            error(f"program_registry '{pid}': no sourceRef (required for program profiles)")
            continue
        if isinstance(source_refs, str):
            source_refs = [source_refs]
        for ref in source_refs:
            if known_sources and ref not in known_sources:
                error(f"program_registry '{pid}': sourceRef '{ref}' not in source_claims.json")


def validate_glossary_sources(known_sources: set):
    path = DATA_DIR / "glossary_terms.json"
    if not path.exists():
        return
    data = load_json(path)
    if not data:
        return
    for term in data.get("terms", []):
        tid = term.get("id", "<no-id>")
        ref = term.get("sourceRef")
        if ref and known_sources and ref not in known_sources:
            error(f"glossary_terms '{tid}': sourceRef '{ref}' not in source_claims.json")


def validate_question_sources(known_sources: set):
    path = DATA_DIR / "question_bank.json"
    if not path.exists():
        return
    data = load_json(path)
    if not data:
        return
    for q in data.get("questions", []):
        qid = q.get("id", "<no-id>")
        ref = q.get("sourceRef")
        if ref and known_sources and ref not in known_sources:
            error(f"question_bank '{qid}': sourceRef '{ref}' not in source_claims.json")


def validate_pages_source_discipline():
    path = DATA_DIR / "pages.json"
    if not path.exists():
        return
    data = load_json(path)
    if not data:
        return
    for p in data.get("pages", []):
        pid = p.get("id", "<no-id>")
        ptype = p.get("type", "")
        if ptype in TECHNICAL_PAGE_TYPES and not p.get("sourceBoundary"):
            error(f"pages.json '{pid}': type '{ptype}' requires a sourceBoundary statement")


def main() -> int:
    print("validate_sources.py")
    print("-" * 40)
    known_sources = load_known_sources()
    if known_sources:
        print(f"  Known sources: {len(known_sources)}")
    else:
        print("  source_claims.json not found or empty — skipping cross-reference checks")
    validate_program_sources(known_sources)
    validate_glossary_sources(known_sources)
    validate_question_sources(known_sources)
    validate_pages_source_discipline()
    if ERRORS:
        print(f"\nSource validation: {len(ERRORS)} error(s) found.")
        return 1
    print("Source validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
