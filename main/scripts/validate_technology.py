#!/usr/bin/env python3
"""Technology Pages Data Quality Validator — Sprint v1B-C."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
TECH_PATH = ROOT / "main" / "data" / "technology_pages.json"
PLACEHOLDER_MARKERS = ["placeholder","todo","tbd","lorem ipsum","insert","answer here"]
PUBLISH_STATUSES = {"published"}

def load_technology() -> list[dict]:
    with open(TECH_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else data.get("pages", [])

def is_placeholder(text: str) -> bool:
    lower = text.lower()
    return any(m in lower for m in PLACEHOLDER_MARKERS)

def validate(pages) -> list[str]:
    errors = []
    seen_ids = {}
    seen_slugs = {}
    for p in pages:
        if p.get("status") not in PUBLISH_STATUSES:
            continue
        pid = p.get("id","")
        slug = p.get("slug","")
        if pid in seen_ids:
            errors.append(f"Duplicate ID '{pid}'")
        else:
            seen_ids[pid] = True
        if slug and slug in seen_slugs:
            errors.append(f"Duplicate slug '{slug}'")
        elif slug:
            seen_slugs[slug] = pid
        # summary
        summary = p.get("summary","").strip()
        if not summary:
            errors.append(f"[{pid}] Missing summary")
        elif is_placeholder(summary):
            errors.append(f"[{pid}] Summary is placeholder")
        elif len(summary) < 100:
            errors.append(f"[{pid}] Summary too short ({len(summary)} chars)")
        # claimBoundary
        cb = p.get("claimBoundary","").strip()
        if not cb:
            errors.append(f"[{pid}] Missing claimBoundary")
        elif is_placeholder(cb):
            errors.append(f"[{pid}] claimBoundary is placeholder")
        # feasibilityBoundary
        fb = p.get("feasibilityBoundary","").strip()
        if not fb:
            errors.append(f"[{pid}] Missing feasibilityBoundary")
        elif is_placeholder(fb):
            errors.append(f"[{pid}] feasibilityBoundary is placeholder")
        # relatedGlossaryTerms
        rgt = p.get("relatedGlossaryTerms",[])
        if len(rgt) < 2:
            errors.append(f"[{pid}] Fewer than 2 relatedGlossaryTerms (has {len(rgt)})")
        # relatedQuestions
        rq = p.get("relatedQuestions",[])
        if len(rq) < 2:
            errors.append(f"[{pid}] Fewer than 2 relatedQuestions (has {len(rq)})")
        # pageLinks
        pl = p.get("pageLinks",[])
        if len(pl) < 2:
            errors.append(f"[{pid}] Fewer than 2 pageLinks (has {len(pl)})")
    return errors

def main() -> int:
    if not TECH_PATH.exists():
        print(f"ERROR: technology_pages.json not found at {TECH_PATH}")
        return 1
    pages = load_technology()
    published = [p for p in pages if p.get("status") in PUBLISH_STATUSES]
    errors = validate(pages)
    print("Technology Pages Quality Report")
    print(f"  Total loaded:      {len(pages)}")
    print(f"  Published:         {len(published)}")
    if errors:
        print()
        for e in errors:
            print(f"ERROR: {e}")
        print()
        print(f"Technology validation: FAIL ({len(errors)} error(s))")
        return 1
    print()
    print("Technology validation: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
