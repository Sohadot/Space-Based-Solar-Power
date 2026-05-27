#!/usr/bin/env python3
"""Schema Validator — confirms all JSON data files conform to required schemas."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "main" / "data"

ERRORS = []


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


APPROVED_STATUSES = {
    "approved_for_launch", "foundation_required", "expansion_cluster_1",
    "expansion_cluster_2", "expansion_cluster_3", "future", "blocked"
}

PAGE_REQUIRED_FIELDS = [
    "id", "slug", "path", "type", "template", "status",
    "sitemap", "navigation", "title", "description",
]


def validate_pages_json():
    path = DATA_DIR / "pages.json"
    if not path.exists():
        error("pages.json: file not found")
        return
    data = load_json(path)
    if not data:
        return

    seen_ids = set()
    seen_paths = set()
    seen_titles = set()

    for p in data.get("pages", []):
        pid = p.get("id", "<no-id>")

        for field in PAGE_REQUIRED_FIELDS:
            if field not in p or p[field] is None or p[field] == "":
                error(f"pages.json page '{pid}': missing required field '{field}'")

        if p.get("status") and p["status"] not in APPROVED_STATUSES:
            error(f"pages.json page '{pid}': unknown status '{p['status']}'")

        if not isinstance(p.get("sitemap"), bool):
            error(f"pages.json page '{pid}': 'sitemap' must be boolean")

        if not isinstance(p.get("navigation"), bool):
            error(f"pages.json page '{pid}': 'navigation' must be boolean")

        desc = p.get("description", "")
        if desc and (len(desc) < 50 or len(desc) > 160):
            error(f"pages.json page '{pid}': description length {len(desc)} not in 50-160 range")

        if pid in seen_ids:
            error(f"pages.json: duplicate id '{pid}'")
        seen_ids.add(pid)

        ppath = p.get("path", "")
        if ppath in seen_paths:
            error(f"pages.json: duplicate path '{ppath}'")
        seen_paths.add(ppath)

        title = p.get("title", "")
        if title in seen_titles and title:
            error(f"pages.json: duplicate title '{title}'")
        seen_titles.add(title)


def validate_glossary_terms():
    path = DATA_DIR / "glossary_terms.json"
    if not path.exists():
        return
    data = load_json(path)
    if not data:
        return
    REQUIRED = ["id", "term", "slug", "path", "domain", "definition", "status"]
    for term in data.get("terms", []):
        tid = term.get("id", "<no-id>")
        for field in REQUIRED:
            if not term.get(field):
                error(f"glossary_terms.json term '{tid}': missing '{field}'")
        if len(term.get("definition", "")) < 50:
            error(f"glossary_terms.json term '{tid}': definition too short")


def validate_question_bank():
    path = DATA_DIR / "question_bank.json"
    if not path.exists():
        return
    data = load_json(path)
    if not data:
        return
    REQUIRED = ["id", "question", "slug", "path", "category", "answer", "status"]
    for q in data.get("questions", []):
        qid = q.get("id", "<no-id>")
        for field in REQUIRED:
            if not q.get(field):
                error(f"question_bank.json question '{qid}': missing '{field}'")
        if len(q.get("answer", "")) < 100:
            error(f"question_bank.json question '{qid}': answer under 100 chars")


def validate_program_registry():
    path = DATA_DIR / "program_registry.json"
    if not path.exists():
        return
    data = load_json(path)
    if not data:
        return
    VALID_STATUSES = {"active", "concluded", "announced", "research_phase",
                     "demonstration_phase", "commercial_phase"}
    REQUIRED = ["id", "programName", "institution", "country", "status", "description"]
    for prog in data.get("programs", []):
        pid = prog.get("id", "<no-id>")
        for field in REQUIRED:
            if not prog.get(field):
                error(f"program_registry.json '{pid}': missing '{field}'")
        if prog.get("status") and prog["status"] not in VALID_STATUSES:
            error(f"program_registry.json '{pid}': unknown status '{prog['status']}'")


def validate_ontology():
    path = DATA_DIR / "ontology.json"
    if not path.exists():
        return
    data = load_json(path)
    if not data:
        return
    VALID_TYPES = {"concept", "technology", "institution", "constraint",
                  "use_case", "region", "person", "standard"}
    node_ids = set()
    for node in data.get("nodes", []):
        nid = node.get("id", "<no-id>")
        if not node.get("label"):
            error(f"ontology.json node '{nid}': missing label")
        if node.get("type") and node["type"] not in VALID_TYPES:
            error(f"ontology.json node '{nid}': unknown type '{node['type']}'")
        if not node.get("definition"):
            error(f"ontology.json node '{nid}': missing definition")
        if nid in node_ids:
            error(f"ontology.json: duplicate node id '{nid}'")
        node_ids.add(nid)
    for rel in data.get("relationships", []):
        if rel.get("from") not in node_ids:
            error(f"ontology.json relationship: unknown 'from' node '{rel.get('from')}'")
        if rel.get("to") not in node_ids:
            error(f"ontology.json relationship: unknown 'to' node '{rel.get('to')}'")


def main() -> int:
    print("validate_schema.py")
    print("-" * 40)
    validate_pages_json()
    validate_glossary_terms()
    validate_question_bank()
    validate_program_registry()
    validate_ontology()
    if ERRORS:
        print(f"\nSchema validation: {len(ERRORS)} error(s) found.")
        return 1
    print("Schema validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
