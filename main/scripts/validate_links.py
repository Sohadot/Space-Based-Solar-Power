#!/usr/bin/env python3
"""Link Validator — confirms all internal links point to existing routes."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "main" / "data"
PUBLIC_DIR = ROOT / "public"

ERRORS = []
BLOCKED_STATUSES = {"blocked", "future", "draft"}


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


def build_published_routes(pages_data: dict) -> set:
    routes = set()
    for p in pages_data.get("pages", []):
        if p.get("status") not in BLOCKED_STATUSES:
            routes.add(p.get("path", ""))
    return routes


def validate_required_links():
    pages_data = load_json(DATA_DIR / "pages.json")
    if not pages_data:
        return

    published = build_published_routes(pages_data)
    blocked_pages = {
        p["path"]
        for p in pages_data.get("pages", [])
        if p.get("status") in BLOCKED_STATUSES
    }

    for p in pages_data.get("pages", []):
        pid = p.get("id", "<no-id>")
        for link in p.get("requiredInternalLinks", []):
            if link in blocked_pages:
                error(f"Page '{pid}': links to blocked/future path '{link}'")
            elif link not in published:
                error(f"Page '{pid}': requiredInternalLink '{link}' not in published routes")


def validate_public_html_links():
    if not PUBLIC_DIR.exists():
        return

    href_pattern = re.compile(r'href="(/[^"#?]*)"')
    published_paths = set()
    for html_file in PUBLIC_DIR.rglob("index.html"):
        relative = html_file.parent.relative_to(PUBLIC_DIR)
        path = "/" + str(relative).replace("\\", "/")
        if path == "/":
            published_paths.add("/")
        else:
            published_paths.add(path + "/")

    for html_file in PUBLIC_DIR.rglob("index.html"):
        content = html_file.read_text(encoding="utf-8")
        for match in href_pattern.finditer(content):
            href = match.group(1)
            if href.startswith("/static"):
                continue
            normalized = href if href.endswith("/") else href + "/"
            if normalized not in published_paths and href not in published_paths:
                error(f"{html_file.relative_to(ROOT)}: broken link '{href}'")


def main() -> int:
    print("validate_links.py")
    print("-" * 40)
    validate_required_links()
    validate_public_html_links()
    if ERRORS:
        print(f"\nLink validation: {len(ERRORS)} error(s) found.")
        return 1
    print("Link validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
