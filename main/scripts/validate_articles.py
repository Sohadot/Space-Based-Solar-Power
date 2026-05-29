#!/usr/bin/env python3
"""Article Pages Data Quality Validator — Sprint v1B-F."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "main" / "data"
ARTICLES_PATH = DATA_DIR / "article_pages.json"
GLOSSARY_PATH = DATA_DIR / "glossary_terms.json"
QUESTIONS_PATH = DATA_DIR / "question_bank.json"
TECH_PATH = DATA_DIR / "technology_pages.json"
PROGRAMS_PATH = DATA_DIR / "program_pages.json"

ALLOWED_CLUSTERS = {
    "infrastructure-strategy",
    "technology-feasibility",
    "institutional-programs",
    "energy-sovereignty-ai",
}

BANNED_PHRASES = [
    "commercially deployed",
    "operational at utility scale",
    "proven infrastructure",
    "ready for deployment",
    "fully demonstrated",
    "sbsp is live",
    "sbsp is working",
]

REQUIRED_FIELDS = [
    "id", "slug", "path", "title", "cluster",
    "summary", "strategicThesis", "institutionalContext",
    "feasibilityBoundary", "claimBoundary", "sourceBoundary",
    "relatedGlossaryTerms", "relatedQuestions",
    "seoTitle", "seoDescription",
]

MIN_SUMMARY_LEN = 150


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def has_banned_phrase(text: str) -> str | None:
    lower = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lower:
            return phrase
    return None


def load_id_set(path: Path, id_field: str, list_key: str = None) -> set:
    if not path.exists():
        return set()
    data = load_json(path)
    items = data if isinstance(data, list) else data.get(list_key, [])
    return {item.get(id_field, "") for item in items if isinstance(item, dict)}


def validate(articles: list, glossary_ids: set, question_ids: set, tech_ids: set, program_ids: set) -> list[str]:
    errors = []
    seen_ids: set = set()
    seen_slugs: set = set()

    for art in articles:
        aid = art.get("id", "<no-id>")
        slug = art.get("slug", "")

        if aid in seen_ids:
            errors.append(f"Duplicate id '{aid}'")
        else:
            seen_ids.add(aid)

        if slug and slug in seen_slugs:
            errors.append(f"[{aid}] Duplicate slug '{slug}'")
        elif slug:
            seen_slugs.add(slug)

        # Required fields
        for field in REQUIRED_FIELDS:
            val = art.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                errors.append(f"[{aid}] Missing or empty required field: '{field}'")
            elif isinstance(val, list) and len(val) == 0:
                errors.append(f"[{aid}] Empty list for required field: '{field}'")

        # Cluster must be allowed
        cluster = art.get("cluster", "")
        if cluster and cluster not in ALLOWED_CLUSTERS:
            errors.append(f"[{aid}] Unknown cluster '{cluster}' — must be one of: {sorted(ALLOWED_CLUSTERS)}")

        # Summary minimum length
        summary = art.get("summary", "").strip()
        if summary and len(summary) < MIN_SUMMARY_LEN:
            errors.append(f"[{aid}] summary too short ({len(summary)} chars, minimum {MIN_SUMMARY_LEN})")

        # seoTitle ≤ 70 chars
        seo_title = art.get("seoTitle", "").strip()
        if seo_title and len(seo_title) > 70:
            errors.append(f"[{aid}] seoTitle too long ({len(seo_title)} chars, max 70)")

        # seoDescription ≤ 160 chars
        seo_desc = art.get("seoDescription", "").strip()
        if seo_desc and len(seo_desc) > 160:
            errors.append(f"[{aid}] seoDescription too long ({len(seo_desc)} chars, max 160)")

        # Banned phrases
        for field_name in ("summary", "strategicThesis", "institutionalContext", "claimBoundary"):
            text = art.get(field_name, "")
            if text:
                phrase = has_banned_phrase(text)
                if phrase:
                    errors.append(f"[{aid}] Banned phrase '{phrase}' in field '{field_name}'")

        # Minimum relatedGlossaryTerms
        rgt = art.get("relatedGlossaryTerms", [])
        if isinstance(rgt, list) and len(rgt) < 3:
            errors.append(f"[{aid}] Fewer than 3 relatedGlossaryTerms (has {len(rgt)})")

        # Minimum relatedQuestions
        rq = art.get("relatedQuestions", [])
        if isinstance(rq, list) and len(rq) < 3:
            errors.append(f"[{aid}] Fewer than 3 relatedQuestions (has {len(rq)})")

        # Cross-reference: glossary terms
        if glossary_ids:
            for gslug in (rgt or []):
                if gslug not in glossary_ids:
                    errors.append(f"[{aid}] relatedGlossaryTerms '{gslug}' not found in glossary_terms.json")

        # Cross-reference: questions
        if question_ids:
            for qid in (rq or []):
                if qid not in question_ids:
                    errors.append(f"[{aid}] relatedQuestions '{qid}' not found in question_bank.json")

        # Cross-reference: technology pages (optional but if present must be valid)
        rtp = art.get("relatedTechnologyPages", [])
        if tech_ids:
            for tpid in (rtp or []):
                if tpid not in tech_ids:
                    errors.append(f"[{aid}] relatedTechnologyPages '{tpid}' not found in technology_pages.json")

        # Cross-reference: programs (optional but if present must be valid)
        rp = art.get("relatedPrograms", [])
        if program_ids:
            for pid in (rp or []):
                if pid not in program_ids:
                    errors.append(f"[{aid}] relatedPrograms '{pid}' not found in program_pages.json")

    # All 4 clusters must be represented
    present_clusters = {art.get("cluster", "") for art in articles}
    for cluster in ALLOWED_CLUSTERS:
        if cluster not in present_clusters:
            errors.append(f"No articles for required cluster '{cluster}' — all 4 clusters must be represented")

    return errors


def main() -> int:
    print("Article Pages Quality Report")
    print("-" * 40)

    if not ARTICLES_PATH.exists():
        print(f"ERROR: article_pages.json not found at {ARTICLES_PATH}")
        return 1

    articles = load_json(ARTICLES_PATH)
    if not isinstance(articles, list):
        articles = articles.get("articles", [])

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

    program_ids: set = set()
    if PROGRAMS_PATH.exists():
        pdata = load_json(PROGRAMS_PATH)
        plist = pdata if isinstance(pdata, list) else pdata.get("programs", [])
        program_ids = {p.get("id", "") for p in plist if isinstance(p, dict)}

    print(f"  Articles loaded:     {len(articles)}")
    print(f"  Glossary terms:      {len(glossary_ids)} known")
    print(f"  Questions:           {len(question_ids)} known")
    print(f"  Technology pages:    {len(tech_ids)} known")
    print(f"  Programs:            {len(program_ids)} known")

    errors = validate(articles, glossary_ids, question_ids, tech_ids, program_ids)

    if errors:
        print()
        for e in errors:
            print(f"ERROR: {e}")
        print()
        print(f"Articles validation: FAIL ({len(errors)} error(s))")
        return 1

    print()
    print("Articles validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
