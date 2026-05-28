#!/usr/bin/env python3
"""Glossary Data Quality Validator — Sprint v1B-A.

Validates all glossary terms with status 'approved' or 'approved_for_launch':
- Term has a substantive definition (non-empty, non-placeholder)
- Term has a claimBoundary
- Term has ≥2 relatedTerms
- Term has ≥1 pageLinks (relatedPages)
- No duplicate IDs or slugs
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GLOSSARY_PATH = ROOT / "main" / "data" / "glossary_terms.json"

PUBLISH_STATUSES = {"approved", "approved_for_launch"}
PLACEHOLDER_MARKERS = [
    "placeholder",
    "todo",
    "tbd",
    "lorem ipsum",
    "insert definition",
    "definition here",
]


def load_terms() -> list[dict]:
    with open(GLOSSARY_PATH, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        return data.get("terms", [])
    return data


def is_placeholder(text: str) -> bool:
    lower = text.lower()
    return any(marker in lower for marker in PLACEHOLDER_MARKERS)


def validate_terms(terms: list[dict]) -> list[str]:
    errors = []
    seen_ids: dict[str, str] = {}
    seen_slugs: dict[str, str] = {}

    for term in terms:
        status = term.get("status", "")
        if status not in PUBLISH_STATUSES:
            continue

        tid = term.get("id", "")
        slug = term.get("slug", "")
        name = term.get("term", tid)

        # Duplicate ID check
        if tid in seen_ids:
            errors.append(f"Duplicate term ID '{tid}' (also on '{seen_ids[tid]}')")
        else:
            seen_ids[tid] = name

        # Duplicate slug check
        if slug and slug in seen_slugs:
            errors.append(f"Duplicate slug '{slug}' (IDs: '{tid}' and '{seen_slugs[slug]}')")
        elif slug:
            seen_slugs[slug] = tid

        # Definition check
        definition = term.get("definition", "").strip()
        if not definition:
            errors.append(f"[{tid}] Missing definition")
        elif is_placeholder(definition):
            errors.append(f"[{tid}] Definition appears to be placeholder text")
        elif len(definition) < 80:
            errors.append(f"[{tid}] Definition too short ({len(definition)} chars); minimum 3 substantive sentences required")

        # claimBoundary check
        claim_boundary = term.get("claimBoundary", "").strip()
        if not claim_boundary:
            errors.append(f"[{tid}] Missing claimBoundary")
        elif is_placeholder(claim_boundary):
            errors.append(f"[{tid}] claimBoundary appears to be placeholder text")

        # relatedTerms check (≥2)
        related_terms = term.get("relatedTerms", [])
        if len(related_terms) < 2:
            errors.append(f"[{tid}] Fewer than 2 relatedTerms (has {len(related_terms)})")

        # pageLinks check (≥1)
        page_links = term.get("pageLinks", [])
        if not page_links:
            errors.append(f"[{tid}] Missing pageLinks (at least 1 required)")

    return errors


def main() -> int:
    if not GLOSSARY_PATH.exists():
        print(f"ERROR: glossary_terms.json not found at {GLOSSARY_PATH}")
        return 1

    terms = load_terms()
    publish_terms = [t for t in terms if t.get("status", "") in PUBLISH_STATUSES]

    errors = validate_terms(terms)

    print("Glossary Quality Report")
    print(f"  Total terms loaded:    {len(terms)}")
    print(f"  Publication-eligible:  {len(publish_terms)}")

    if errors:
        print()
        for err in errors:
            print(f"ERROR: {err}")
        print()
        print(f"Glossary validation: FAIL ({len(errors)} error(s))")
        return 1

    print()
    print("Glossary validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
