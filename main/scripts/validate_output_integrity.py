#!/usr/bin/env python3
"""Output Integrity Validator — Sprint 2B.

Checks:
- No legacy ref-nav patterns in any generated HTML
- Hub pages have populated child links
- Hub pages have non-empty main containers
- Reports page counts, hub link counts, sitemap and robots.txt state
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DIR = ROOT / "public"

LEGACY_PATTERNS = [
    ('<nav class="ref-nav"', "ref-nav class"),
    ('aria-label="Explore"', 'aria-label="Explore"'),
    ('aria-label="Related pages"', 'aria-label="Related pages"'),
    ("ref-nav-label", "ref-nav-label class"),
]

HUBS = [
    (PUBLIC_DIR / "glossary" / "index.html", "/glossary/", "glossary"),
    (PUBLIC_DIR / "questions" / "index.html", "/questions/", "questions"),
    (PUBLIC_DIR / "programs" / "index.html", "/programs/", "programs"),
]


def collect_html_files() -> list[Path]:
    return sorted(PUBLIC_DIR.rglob("*.html"))


def check_legacy_nav(html_files: list[Path]) -> list[str]:
    errors = []
    for pattern, label in LEGACY_PATTERNS:
        hits = [f for f in html_files if pattern in f.read_text(encoding="utf-8")]
        if hits:
            sample = [str(f.relative_to(ROOT)) for f in hits[:5]]
            extra = f" (and {len(hits) - 5} more)" if len(hits) > 5 else ""
            errors.append(
                f"Legacy pattern '{label}' found in {len(hits)} file(s):\n    "
                + "\n    ".join(sample) + extra
            )
    return errors


def check_hub(hub_path: Path, child_prefix: str, name: str) -> tuple[list[str], int]:
    errors = []
    if not hub_path.exists():
        errors.append(f"{name} hub missing: {hub_path.relative_to(ROOT)}")
        return errors, 0

    content = hub_path.read_text(encoding="utf-8")

    # Count distinct child page links (exclude the hub itself)
    child_links = re.findall(
        rf'href="({re.escape(child_prefix)}[^/"]+/)"',
        content,
    )
    unique_children = set(child_links)
    if not unique_children:
        errors.append(f"{name} hub has no links to child pages")

    # Check main container is not near-empty
    main_match = re.search(r"<main[^>]*>(.*?)</main>", content, re.DOTALL)
    if main_match:
        main_text = re.sub(r"<[^>]+>", "", main_match.group(1)).strip()
        if len(main_text) < 50:
            errors.append(f"{name} hub main container is near-empty ({len(main_text)} chars of text)")

    return errors, len(unique_children)


def count_child_pages(prefix: str, html_files: list[Path]) -> int:
    prefix_dir = PUBLIC_DIR / prefix
    return sum(
        1 for f in html_files
        if f.name == "index.html"
        and f.parent != prefix_dir
        and prefix_dir in f.parents
    )


def check_sitemap_and_robots() -> tuple[bool, bool, bool]:
    sitemap = PUBLIC_DIR / "sitemap.xml"
    robots = PUBLIC_DIR / "robots.txt"
    sitemap_exists = sitemap.exists()
    robots_exists = robots.exists()
    robots_ref = False
    if robots_exists:
        robots_ref = "sitemap.xml" in robots.read_text(encoding="utf-8")
    return sitemap_exists, robots_exists, robots_ref


def main() -> int:
    html_files = collect_html_files()
    all_pages = [f for f in html_files if f.name == "index.html"]

    errors = []

    legacy_errors = check_legacy_nav(html_files)
    errors.extend(legacy_errors)

    glossary_count = questions_count = programs_count = 0
    hub_link_counts = {}
    for hub_path, prefix, name in HUBS:
        hub_errors, link_count = check_hub(hub_path, prefix, name)
        errors.extend(hub_errors)
        hub_link_counts[name] = link_count
        if name == "glossary":
            glossary_count = count_child_pages("glossary", html_files)
        elif name == "questions":
            questions_count = count_child_pages("questions", html_files)
        elif name == "programs":
            programs_count = count_child_pages("programs", html_files)

    legacy_match_total = sum(
        1 for pattern, _ in LEGACY_PATTERNS
        for f in html_files
        if pattern in f.read_text(encoding="utf-8")
    )

    sitemap_ok, robots_ok, robots_ref = check_sitemap_and_robots()

    print("Output Integrity Report")
    print(f"  Total HTML pages:          {len(all_pages)}")
    print(f"  Glossary child pages:      {glossary_count}")
    print(f"  Question child pages:      {questions_count}")
    print(f"  Program child pages:       {programs_count}")
    print(f"  Glossary hub links:        {hub_link_counts.get('glossary', 0)}")
    print(f"  Questions hub links:       {hub_link_counts.get('questions', 0)}")
    print(f"  Programs hub links:        {hub_link_counts.get('programs', 0)}")
    print(f"  Legacy nav matches:        {legacy_match_total}")
    print(f"  sitemap.xml exists:        {sitemap_ok}")
    print(f"  robots.txt sitemap target: {robots_ref}")

    if errors:
        print()
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    print()
    print("Output integrity: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
