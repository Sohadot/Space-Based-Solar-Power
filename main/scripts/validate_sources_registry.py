#!/usr/bin/env python3
"""Source Registry Validator — governed evidence registry quality checks (v1B-E)."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "main" / "data"
REGISTRY_PATH = DATA_DIR / "source_registry.json"

ALLOWED_SOURCE_CLASSES = {
    "institutional-space-agency",
    "government-policy",
    "academic-research",
    "technical-standard",
    "industry-consortium",
    "historical-primary",
    "methodology-internal",
}

REQUIRED_FIELDS = [
    "id",
    "slug",
    "label",
    "source_class",
    "authority_role",
    "claim_scope",
    "verification_posture",
    "related_page_types",
    "boundary_notes",
]

BANNED_VAGUE_AUTHORITY = [
    "proves that",
    "confirms that sbsp works",
    "confirms commercial viability",
    "established fact",
    "widely accepted truth",
    "definitively shows",
    "conclusively proves",
    "industry consensus that sbsp is ready",
]

MIN_CLAIM_SCOPE_LEN = 60
MIN_BOUNDARY_NOTES_LEN = 40


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def has_banned_phrase(text: str) -> str | None:
    lower = text.lower()
    for phrase in BANNED_VAGUE_AUTHORITY:
        if phrase in lower:
            return phrase
    return None


def validate(records: list) -> list[str]:
    errors = []
    seen_ids: set = set()
    seen_slugs: set = set()

    class_counts: dict[str, int] = {}

    for rec in records:
        rid = rec.get("id", "<no-id>")

        # Duplicate ID
        if rid in seen_ids:
            errors.append(f"Duplicate id '{rid}'")
        else:
            seen_ids.add(rid)

        # Duplicate slug
        slug = rec.get("slug", "")
        if slug and slug in seen_slugs:
            errors.append(f"[{rid}] Duplicate slug '{slug}'")
        elif slug:
            seen_slugs.add(slug)

        # Required fields
        for field in REQUIRED_FIELDS:
            val = rec.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                errors.append(f"[{rid}] Missing or empty required field: '{field}'")
            elif isinstance(val, list) and len(val) == 0:
                errors.append(f"[{rid}] Empty list for required field: '{field}'")

        # Allowed source class
        sc = rec.get("source_class", "")
        if sc and sc not in ALLOWED_SOURCE_CLASSES:
            errors.append(f"[{rid}] Unknown source_class '{sc}' — must be one of: {sorted(ALLOWED_SOURCE_CLASSES)}")
        elif sc:
            class_counts[sc] = class_counts.get(sc, 0) + 1

        # Minimum claim_scope length
        cs = rec.get("claim_scope", "").strip()
        if cs and len(cs) < MIN_CLAIM_SCOPE_LEN:
            errors.append(f"[{rid}] claim_scope too short ({len(cs)} chars, minimum {MIN_CLAIM_SCOPE_LEN})")

        # Minimum boundary_notes length
        bn = rec.get("boundary_notes", "").strip()
        if bn and len(bn) < MIN_BOUNDARY_NOTES_LEN:
            errors.append(f"[{rid}] boundary_notes too short ({len(bn)} chars, minimum {MIN_BOUNDARY_NOTES_LEN})")

        # Banned vague authority language
        for field_name in ("claim_scope", "boundary_notes", "authority_role", "verification_posture"):
            text = rec.get(field_name, "")
            if text:
                phrase = has_banned_phrase(text)
                if phrase:
                    errors.append(f"[{rid}] Banned vague authority phrase '{phrase}' in field '{field_name}'")

        # related_page_types must be a non-empty list
        rpt = rec.get("related_page_types", [])
        if not isinstance(rpt, list) or len(rpt) == 0:
            errors.append(f"[{rid}] related_page_types must be a non-empty list")

    # All 7 source classes must be represented
    for sc in ALLOWED_SOURCE_CLASSES:
        if sc not in class_counts:
            errors.append(f"No records for required source_class '{sc}' — all 7 classes must be represented")

    return errors, class_counts


def main() -> int:
    print("Source Registry Quality Report")
    print("-" * 40)

    if not REGISTRY_PATH.exists():
        print(f"ERROR: source_registry.json not found at {REGISTRY_PATH}")
        return 1

    records = load_json(REGISTRY_PATH)
    if not isinstance(records, list):
        records = records.get("sources", [])

    print(f"  Records loaded: {len(records)}")

    errors, class_counts = validate(records)

    print("  Source classes present:")
    for sc in sorted(ALLOWED_SOURCE_CLASSES):
        count = class_counts.get(sc, 0)
        status = "✓" if count > 0 else "✗ MISSING"
        print(f"    {sc}: {count} {status}")

    if errors:
        print()
        for e in errors:
            print(f"ERROR: {e}")
        print()
        print(f"Source registry validation: FAIL ({len(errors)} error(s))")
        return 1

    print()
    print("Source registry validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
