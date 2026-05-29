#!/usr/bin/env python3
"""Program Pages Data Quality Validator — Sprint v1B-D."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROG_PATH = ROOT / "main" / "data" / "program_pages.json"
GLOSSARY_PATH = ROOT / "main" / "data" / "glossary_terms.json"
QUESTIONS_PATH = ROOT / "main" / "data" / "question_bank.json"
TECH_PATH = ROOT / "main" / "data" / "technology_pages.json"

BANNED_PHRASES = [
    "commercially deployed",
    "operational at utility scale",
    "proven infrastructure",
    "ready for deployment",
    "fully demonstrated",
]

REQUIRED_FIELDS = [
    "id", "slug", "title", "institution", "country_or_region",
    "program_status", "activity_type", "cluster", "summary",
    "institutional_context", "sbsp_relevance", "technology_relationship",
    "feasibility_boundary", "claim_boundary", "related_glossary_terms",
    "related_questions", "source_footer", "seoTitle", "seoDescription",
]

HISTORICAL_TYPES = {"historical_reference"}


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_known_ids(path: Path, id_field: str, list_key: str = None) -> set:
    if not path.exists():
        return set()
    data = load_json(path)
    if isinstance(data, list):
        items = data
    elif list_key:
        items = data.get(list_key, [])
    else:
        items = data
    return {item.get(id_field, item.get("id", "")) for item in items if isinstance(item, dict)}


def has_banned_phrase(text: str) -> str | None:
    lower = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lower:
            return phrase
    return None


def validate(programs: list, glossary_ids: set, question_ids: set, tech_ids: set) -> list[str]:
    errors = []
    seen_ids: dict = {}
    seen_slugs: dict = {}

    for p in programs:
        pid = p.get("id", "<no-id>")
        slug = p.get("slug", "")
        activity_type = p.get("activity_type", "")

        # Duplicate ID check
        if pid in seen_ids:
            errors.append(f"Duplicate ID '{pid}'")
        else:
            seen_ids[pid] = True

        # Duplicate slug check
        if slug and slug in seen_slugs:
            errors.append(f"Duplicate slug '{slug}'")
        elif slug:
            seen_slugs[slug] = pid

        # Required fields
        for field in REQUIRED_FIELDS:
            val = p.get(field)
            if val is None or (isinstance(val, str) and not val.strip()) or (isinstance(val, list) and len(val) == 0):
                errors.append(f"[{pid}] Missing or empty required field: {field}")

        # Summary minimum length
        summary = p.get("summary", "").strip()
        if summary and len(summary) < 150:
            errors.append(f"[{pid}] Summary too short ({len(summary)} chars, minimum 150)")

        # Banned overclaim language checks
        for field_name in ("summary", "institutional_context", "sbsp_relevance", "claim_boundary"):
            text = p.get(field_name, "")
            if text:
                phrase = has_banned_phrase(text)
                if phrase:
                    errors.append(f"[{pid}] Banned overclaim phrase '{phrase}' in field '{field_name}'")

        # Minimum glossary term links
        rgt = p.get("related_glossary_terms", [])
        if isinstance(rgt, list) and len(rgt) < 2:
            errors.append(f"[{pid}] Fewer than 2 related_glossary_terms (has {len(rgt)})")

        # Minimum question links
        rq = p.get("related_questions", [])
        if isinstance(rq, list) and len(rq) < 2:
            errors.append(f"[{pid}] Fewer than 2 related_questions (has {len(rq)})")

        # Minimum technology page links (skip for historical_reference)
        rtp = p.get("related_technology_pages", [])
        if activity_type not in HISTORICAL_TYPES and isinstance(rtp, list) and len(rtp) < 1:
            errors.append(f"[{pid}] No related_technology_pages (required for non-historical entries)")

        # Cross-reference: glossary terms
        if glossary_ids:
            for gslug in (rgt or []):
                if gslug not in glossary_ids:
                    errors.append(f"[{pid}] related_glossary_terms '{gslug}' not found in glossary_terms.json")

        # Cross-reference: questions
        if question_ids:
            for qid in (rq or []):
                if qid not in question_ids:
                    errors.append(f"[{pid}] related_questions '{qid}' not found in question_bank.json")

        # Cross-reference: technology pages
        if tech_ids:
            for tpid in (rtp or []):
                if tpid not in tech_ids:
                    errors.append(f"[{pid}] related_technology_pages '{tpid}' not found in technology_pages.json")

        # Source footer non-empty
        sf = p.get("source_footer", "").strip()
        if not sf:
            errors.append(f"[{pid}] source_footer is empty")

    return errors


def main() -> int:
    if not PROG_PATH.exists():
        print(f"ERROR: program_pages.json not found at {PROG_PATH}")
        return 1

    programs = load_json(PROG_PATH)
    if not isinstance(programs, list):
        programs = programs.get("programs", [])

    # Load cross-reference sets
    glossary_ids: set = set()
    if GLOSSARY_PATH.exists():
        gdata = load_json(GLOSSARY_PATH)
        glist = gdata if isinstance(gdata, list) else gdata.get("terms", [])
        glossary_ids = {t.get("slug", t.get("id", "")) for t in glist if isinstance(t, dict)}

    question_ids: set = set()
    if QUESTIONS_PATH.exists():
        qdata = load_json(QUESTIONS_PATH)
        qlist = qdata if isinstance(qdata, list) else qdata.get("questions", [])
        question_ids = {q.get("id", "") for q in qlist if isinstance(q, dict)}

    tech_ids: set = set()
    if TECH_PATH.exists():
        tdata = load_json(TECH_PATH)
        tlist = tdata if isinstance(tdata, list) else tdata.get("pages", [])
        tech_ids = {t.get("id", "") for t in tlist if isinstance(t, dict)}

    errors = validate(programs, glossary_ids, question_ids, tech_ids)

    print("Program Pages Quality Report")
    print(f"  Total loaded:      {len(programs)}")
    print(f"  Glossary terms:    {len(glossary_ids)} known")
    print(f"  Questions:         {len(question_ids)} known")
    print(f"  Technology pages:  {len(tech_ids)} known")

    if errors:
        print()
        for e in errors:
            print(f"ERROR: {e}")
        print()
        print(f"Programs validation: FAIL ({len(errors)} error(s))")
        return 1

    print()
    print("Programs validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
