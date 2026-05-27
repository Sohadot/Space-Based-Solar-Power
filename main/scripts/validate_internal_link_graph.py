#!/usr/bin/env python3
"""Internal Link Graph Validator — enforces graph integrity, prevents orphan pages."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "main" / "data"
PUBLIC_DIR = ROOT / "public"

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


def build_inbound_index(pages_data: dict) -> dict:
    inbound = {}
    approved = {"approved_for_launch"}
    for p in pages_data.get("pages", []):
        if p.get("status") in approved:
            inbound[p["path"]] = set()

    for p in pages_data.get("pages", []):
        if p.get("status") not in approved:
            continue
        source_path = p["path"]
        for link in p.get("requiredInternalLinks", []):
            if link in inbound:
                inbound[link].add(source_path)

    return inbound


def validate_no_orphans(inbound: dict):
    HOME = "/"
    for path, sources in inbound.items():
        if path == HOME:
            continue
        if len(sources) == 0:
            error(f"Orphan page: '{path}' has no inbound links from approved pages")


def validate_required_hub_links(pages_data: dict, graph_data: dict):
    rules_by_type = {r["pageType"]: r for r in graph_data.get("rules", [])}
    approved = {"approved_for_launch"}

    for p in pages_data.get("pages", []):
        if p.get("status") not in approved:
            continue
        pid = p.get("id", "<no-id>")
        ptype = p.get("type", "")
        page_path = p.get("path", "")
        rule = rules_by_type.get(ptype)
        if not rule:
            continue

        required_links = set(rule.get("requiredOutboundLinks", []))
        required_links.discard(page_path)  # A page must not require a self-link
        page_links = set(p.get("requiredInternalLinks", []))
        missing = required_links - page_links
        for m in missing:
            error(f"Page '{pid}' (type: {ptype}): missing required hub link '{m}'")

        trust_page = rule.get("trustPage")
        if trust_page and trust_page not in page_links:
            error(f"Page '{pid}' (type: {ptype}): missing trust page link '{trust_page}'")


def validate_hub_outbound_budgets(graph_data: dict, pages_data: dict):
    hub_defs = graph_data.get("hubDefinitions", {})
    approved = {"approved_for_launch"}

    for hub_path, hub_conf in hub_defs.items():
        max_links = hub_conf.get("maxOutboundLinks", 999)
        outbound_count = 0
        for p in pages_data.get("pages", []):
            if p.get("status") not in approved:
                continue
            if p["path"] == hub_path:
                outbound_count = len(p.get("requiredInternalLinks", []))
                break
        if outbound_count > max_links:
            error(f"Hub '{hub_path}': outbound links ({outbound_count}) exceed budget ({max_links})")


def validate_forbidden_anchor_texts():
    if not PUBLIC_DIR.exists():
        return
    graph_data = load_json(DATA_DIR / "internal_link_graph.json")
    if not graph_data:
        return
    forbidden = graph_data.get("linkTextRules", {}).get("forbiddenAnchorTexts", [])
    anchor_pattern = re.compile(r"<a[^>]*>([^<]+)</a>", re.IGNORECASE)
    for html_file in PUBLIC_DIR.rglob("index.html"):
        content = html_file.read_text(encoding="utf-8")
        for match in anchor_pattern.finditer(content):
            anchor_text = match.group(1).strip().lower()
            if anchor_text in forbidden:
                error(f"{html_file.relative_to(ROOT)}: forbidden anchor text '{anchor_text}'")


def main() -> int:
    print("validate_internal_link_graph.py")
    print("-" * 40)

    pages_data = load_json(DATA_DIR / "pages.json")
    graph_data = load_json(DATA_DIR / "internal_link_graph.json")

    if not pages_data or not graph_data:
        print("  Cannot validate: missing pages.json or internal_link_graph.json")
        return 1

    inbound = build_inbound_index(pages_data)
    validate_no_orphans(inbound)
    validate_required_hub_links(pages_data, graph_data)
    validate_hub_outbound_budgets(graph_data, pages_data)
    validate_forbidden_anchor_texts()

    if ERRORS:
        print(f"\nLink graph validation: {len(ERRORS)} error(s) found.")
        return 1
    print("Link graph validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
