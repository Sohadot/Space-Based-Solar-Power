#!/usr/bin/env python3
"""Tool Pages Data Quality Validator — Sprint v1B-H."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "main" / "data"
TOOLS_PATH = DATA_DIR / "tool_pages.json"
GLOSSARY_PATH = DATA_DIR / "glossary_terms.json"
QUESTIONS_PATH = DATA_DIR / "question_bank.json"
TECH_PATH = DATA_DIR / "technology_pages.json"
PROGRAMS_PATH = DATA_DIR / "program_pages.json"
ARTICLES_PATH = DATA_DIR / "article_pages.json"

REQUIRED_FIELDS = [
    "id", "slug", "path", "title", "toolType",
    "strategicPurpose", "userAudience", "decisionValue",
    "methodologyBoundary", "claimBoundary", "sourceBoundary",
    "evaluationDimensions", "outputInterpretation",
    "relatedGlossaryTerms", "relatedQuestions",
    "seoTitle", "seoDescription",
]

ALLOWED_TOOL_TYPES = {
    "readiness-matrix",
    "classification-reference",
    "comparison-reference",
    "dependency-reference",
    "strategic-positioning",
    "evidence-reference",
}

BANNED_PHRASES = [
    "javascript",
    "click here to calculate",
    "enter your values",
    "real-time simulation",
    "live data",
    "coming soon",
    "placeholder",
    "under construction",
    "commercially deployed",
    "operational at utility scale",
    "proven infrastructure",
    "ready for deployment",
    "fully demonstrated",
    "sbsp is live",
    "sbsp is working",
    "will definitely",
    "is guaranteed",
    "fake interactive",
]

MIN_PURPOSE_LEN = 150
MIN_VALUE_LEN = 80


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def has_banned_phrase(text: str) -> str | None:
    lower = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lower:
            return phrase
    return None


def load_id_set(path: Path, id_field: str, list_key: str | None = None) -> set:
    if not path.exists():
        return set()
    data = load_json(path)
    items = data if isinstance(data, list) else data.get(list_key, [])
    return {item.get(id_field, "") for item in items if isinstance(item, dict)}


def validate(tools: list, glossary_ids: set, question_ids: set,
             tech_ids: set, program_ids: set, article_ids: set) -> list[str]:
    errors = []
    seen_ids: set = set()
    seen_slugs: set = set()

    for tool in tools:
        tid = tool.get("id", "<no-id>")
        slug = tool.get("slug", "")

        if tid in seen_ids:
            errors.append(f"Duplicate id '{tid}'")
        else:
            seen_ids.add(tid)

        if slug and slug in seen_slugs:
            errors.append(f"[{tid}] Duplicate slug '{slug}'")
        elif slug:
            seen_slugs.add(slug)

        # Required fields
        for field in REQUIRED_FIELDS:
            val = tool.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                errors.append(f"[{tid}] Missing or empty required field: '{field}'")
            elif isinstance(val, list) and len(val) == 0:
                errors.append(f"[{tid}] Empty list for required field: '{field}'")

        # toolType must be allowed
        tool_type = tool.get("toolType", "")
        if tool_type and tool_type not in ALLOWED_TOOL_TYPES:
            errors.append(f"[{tid}] Unknown toolType '{tool_type}' — allowed: {sorted(ALLOWED_TOOL_TYPES)}")

        # strategicPurpose minimum length
        purpose = tool.get("strategicPurpose", "").strip()
        if purpose and len(purpose) < MIN_PURPOSE_LEN:
            errors.append(f"[{tid}] strategicPurpose too short ({len(purpose)} chars, minimum {MIN_PURPOSE_LEN})")

        # decisionValue minimum length
        dv = tool.get("decisionValue", "").strip()
        if dv and len(dv) < MIN_VALUE_LEN:
            errors.append(f"[{tid}] decisionValue too short ({len(dv)} chars, minimum {MIN_VALUE_LEN})")

        # seoTitle ≤ 70 chars
        seo_title = tool.get("seoTitle", "").strip()
        if seo_title and len(seo_title) > 70:
            errors.append(f"[{tid}] seoTitle too long ({len(seo_title)} chars, max 70)")

        # seoDescription ≤ 160 chars
        seo_desc = tool.get("seoDescription", "").strip()
        if seo_desc and len(seo_desc) > 160:
            errors.append(f"[{tid}] seoDescription too long ({len(seo_desc)} chars, max 160)")

        # Banned phrases across governed text fields
        for field_name in ("strategicPurpose", "decisionValue", "methodologyBoundary",
                           "claimBoundary", "sourceBoundary", "outputInterpretation"):
            text = tool.get(field_name, "")
            if text:
                phrase = has_banned_phrase(text)
                if phrase:
                    errors.append(f"[{tid}] Banned phrase '{phrase}' in field '{field_name}'")

        # Minimum relatedGlossaryTerms
        rgt = tool.get("relatedGlossaryTerms", [])
        if isinstance(rgt, list) and len(rgt) < 3:
            errors.append(f"[{tid}] Fewer than 3 relatedGlossaryTerms (has {len(rgt)})")

        # Minimum relatedQuestions
        rq = tool.get("relatedQuestions", [])
        if isinstance(rq, list) and len(rq) < 2:
            errors.append(f"[{tid}] Fewer than 2 relatedQuestions (has {len(rq)})")

        # Minimum relatedTechnologyPages (at least 1 where present)
        rtp = tool.get("relatedTechnologyPages", [])
        if isinstance(rtp, list) and len(rtp) == 0:
            errors.append(f"[{tid}] No relatedTechnologyPages — each tool should reference at least 1")

        # evaluationDimensions must be non-empty list of dicts
        ev = tool.get("evaluationDimensions", [])
        if not isinstance(ev, list) or len(ev) == 0:
            errors.append(f"[{tid}] evaluationDimensions is empty or not a list")
        else:
            for i, dim in enumerate(ev):
                if not isinstance(dim, dict):
                    errors.append(f"[{tid}] evaluationDimensions[{i}] is not an object")
                elif not dim:
                    errors.append(f"[{tid}] evaluationDimensions[{i}] is empty")

        # Cross-reference: glossary terms
        if glossary_ids:
            for gslug in (rgt or []):
                if gslug not in glossary_ids:
                    errors.append(f"[{tid}] relatedGlossaryTerms '{gslug}' not found in glossary_terms.json")

        # Cross-reference: questions
        if question_ids:
            for qid in (rq or []):
                if qid not in question_ids:
                    errors.append(f"[{tid}] relatedQuestions '{qid}' not found in question_bank.json")

        # Cross-reference: technology pages
        if tech_ids:
            for tpid in (rtp or []):
                if tpid not in tech_ids:
                    errors.append(f"[{tid}] relatedTechnologyPages '{tpid}' not found in technology_pages.json")

        # Cross-reference: programs (optional)
        rp = tool.get("relatedPrograms", [])
        if program_ids:
            for pid in (rp or []):
                if pid not in program_ids:
                    errors.append(f"[{tid}] relatedPrograms '{pid}' not found in program_pages.json")

        # Cross-reference: articles (optional)
        ra = tool.get("relatedArticles", [])
        if article_ids:
            for aid in (ra or []):
                if aid not in article_ids:
                    errors.append(f"[{tid}] relatedArticles '{aid}' not found in article_pages.json")

        # Path must start with /tools/
        path = tool.get("path", "")
        if path and not path.startswith("/tools/"):
            errors.append(f"[{tid}] path '{path}' does not start with /tools/")

    return errors


def main() -> int:
    print("Tool Pages Quality Report")
    print("-" * 40)

    if not TOOLS_PATH.exists():
        print(f"ERROR: tool_pages.json not found at {TOOLS_PATH}")
        return 1

    tools = load_json(TOOLS_PATH)
    if not isinstance(tools, list):
        tools = tools.get("tools", [])

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

    article_ids: set = set()
    if ARTICLES_PATH.exists():
        adata = load_json(ARTICLES_PATH)
        alist = adata if isinstance(adata, list) else adata.get("articles", [])
        article_ids = {a.get("id", "") for a in alist if isinstance(a, dict)}

    print(f"  Tools loaded:          {len(tools)}")
    print(f"  Glossary terms:        {len(glossary_ids)} known")
    print(f"  Questions:             {len(question_ids)} known")
    print(f"  Technology pages:      {len(tech_ids)} known")
    print(f"  Programs:              {len(program_ids)} known")
    print(f"  Articles:              {len(article_ids)} known")

    errors = validate(tools, glossary_ids, question_ids, tech_ids, program_ids, article_ids)

    if errors:
        print()
        for e in errors:
            print(f"ERROR: {e}")
        print()
        print(f"Tools validation: FAIL ({len(errors)} error(s))")
        return 1

    print()
    print("Tools validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
