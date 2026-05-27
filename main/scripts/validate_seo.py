#!/usr/bin/env python3
"""SEO Validator — confirms title, description, H1, canonical on all pages."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "main" / "data"
PUBLIC_DIR = ROOT / "public"

ERRORS = []
DOMAIN = "space-based-solar-power.com"


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


def validate_pages_seo_fields():
    """Validate SEO fields in pages.json before build."""
    pages_data = load_json(DATA_DIR / "pages.json")
    if not pages_data:
        return
    approved = {"approved_for_launch"}
    for p in pages_data.get("pages", []):
        if p.get("status") not in approved:
            continue
        pid = p.get("id", "<no-id>")
        title = p.get("title", "")
        desc = p.get("description", "")
        slug = p.get("slug", "")

        if not title:
            error(f"pages.json '{pid}': missing title")
        elif len(title) > 70:
            error(f"pages.json '{pid}': title too long ({len(title)} chars, max 70)")

        if not desc:
            error(f"pages.json '{pid}': missing description")
        elif len(desc) < 50:
            error(f"pages.json '{pid}': description too short ({len(desc)} chars)")
        elif len(desc) > 160:
            error(f"pages.json '{pid}': description too long ({len(desc)} chars)")

        if " " in slug:
            error(f"pages.json '{pid}': slug contains spaces")


def validate_generated_html_seo():
    """Validate SEO tags in generated HTML files."""
    if not PUBLIC_DIR.exists():
        return

    title_pattern = re.compile(r"<title>(.+?)</title>", re.DOTALL)
    desc_pattern = re.compile(r'<meta name="description" content="(.+?)"')
    canonical_pattern = re.compile(r'<link rel="canonical" href="(.+?)"')
    h1_pattern = re.compile(r"<h1[^>]*>(.+?)</h1>", re.DOTALL)

    for html_file in PUBLIC_DIR.rglob("index.html"):
        content = html_file.read_text(encoding="utf-8")
        rel = html_file.relative_to(ROOT)

        titles = title_pattern.findall(content)
        if not titles:
            error(f"{rel}: missing <title>")
        elif len(titles[0].strip()) > 70:
            error(f"{rel}: title too long ({len(titles[0].strip())} chars)")

        descs = desc_pattern.findall(content)
        if not descs:
            error(f"{rel}: missing <meta name='description'>")
        elif len(descs[0]) < 50 or len(descs[0]) > 160:
            error(f"{rel}: description length {len(descs[0])} not in 50-160 range")

        canonicals = canonical_pattern.findall(content)
        if not canonicals:
            error(f"{rel}: missing <link rel='canonical'>")
        elif DOMAIN not in canonicals[0]:
            error(f"{rel}: canonical does not reference {DOMAIN}")

        h1s = h1_pattern.findall(content)
        if not h1s:
            error(f"{rel}: missing <h1>")
        elif len(h1s) > 1:
            error(f"{rel}: multiple <h1> tags ({len(h1s)} found)")


def main() -> int:
    print("validate_seo.py")
    print("-" * 40)
    validate_pages_seo_fields()
    validate_generated_html_seo()
    if ERRORS:
        print(f"\nSEO validation: {len(ERRORS)} error(s) found.")
        return 1
    print("SEO validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
