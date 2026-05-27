#!/usr/bin/env python3
"""Claim Validator — blocks unsourced certainty claims on high-risk page types."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "main" / "data"
CONTENT_DIR = ROOT / "main" / "content" / "pages"

ERRORS = []

HIGH_RISK_TYPES = {
    "constraint_page", "technical_reference", "country_profile",
    "program_profile", "claim_review", "source_brief",
}

CERTAINTY_PATTERNS = [
    r"will achieve",
    r"is guaranteed",
    r"has been proven",
    r"definitively",
    r"will definitely",
    r"is certain to",
    r"without doubt",
    r"100% efficient",
    r"will solve",
]
COMPILED = [re.compile(p, re.IGNORECASE) for p in CERTAINTY_PATTERNS]


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


def extract_all_text(obj) -> str:
    parts = []
    if isinstance(obj, str):
        return obj
    if isinstance(obj, list):
        return " ".join(extract_all_text(v) for v in obj)
    if isinstance(obj, dict):
        return " ".join(extract_all_text(v) for v in obj.values())
    return ""


def validate_high_risk_pages():
    pages_data = load_json(DATA_DIR / "pages.json")
    if not pages_data:
        return
    for p in pages_data.get("pages", []):
        pid = p.get("id", "<no-id>")
        ptype = p.get("type", "")
        if ptype not in HIGH_RISK_TYPES:
            continue
        if not p.get("claimBoundary") and not p.get("sourceBoundary"):
            error(f"pages.json '{pid}': high-risk type '{ptype}' missing claimBoundary/sourceBoundary")


def validate_content_certainty_claims():
    if not CONTENT_DIR.exists():
        return
    for json_file in CONTENT_DIR.glob("*.json"):
        data = load_json(json_file)
        if not data:
            continue
        text = extract_all_text(data)
        for pattern in COMPILED:
            if pattern.search(text):
                error(f"{json_file.name}: forbidden certainty phrase '{pattern.pattern}' — requires source citation")


def validate_comparison_pages():
    path = DATA_DIR / "comparison_matrix.json"
    if not path.exists():
        return
    data = load_json(path)
    if not data:
        return
    SUPERIORITY_PATTERNS = [
        re.compile(r"is better than", re.IGNORECASE),
        re.compile(r"is superior to", re.IGNORECASE),
        re.compile(r"is worse than", re.IGNORECASE),
        re.compile(r"is clearly the best", re.IGNORECASE),
    ]
    for comp in data.get("comparisons", []):
        cid = comp.get("id", "<no-id>")
        if not comp.get("sourceBoundary") and not comp.get("claimBoundary"):
            error(f"comparison_matrix '{cid}': missing sourceBoundary or claimBoundary")
        text = extract_all_text(comp)
        for pattern in SUPERIORITY_PATTERNS:
            if pattern.search(text) and not comp.get("sourceRef"):
                error(f"comparison_matrix '{cid}': superiority claim without sourceRef")


def main() -> int:
    print("validate_claims.py")
    print("-" * 40)
    validate_high_risk_pages()
    validate_content_certainty_claims()
    validate_comparison_pages()
    if ERRORS:
        print(f"\nClaim validation: {len(ERRORS)} error(s) found.")
        return 1
    print("Claim validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
