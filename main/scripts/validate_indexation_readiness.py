#!/usr/bin/env python3
"""Indexation Readiness Validator — Sprint v1B-G.

Checks all structural requirements for eventual Google Search Console submission:
sitemap integrity, canonical correctness, robots.txt, hub discoverability,
no-noindex guarantees, orphan detection, and legacy nav pattern absence.
Does NOT submit to GSC — that action remains explicitly blocked.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DIR = ROOT / "public"
DATA_DIR = ROOT / "main" / "data"

DOMAIN = "https://space-based-solar-power.com"

CANONICAL_SITEMAP_URL = f"{DOMAIN}/sitemap.xml"
SITEMAP_INDEX = PUBLIC_DIR / "sitemap_index.xml"
SITEMAP_XML = PUBLIC_DIR / "sitemap.xml"
ROBOTS_TXT = PUBLIC_DIR / "robots.txt"

REQUIRED_HUBS = [
    "/glossary/",
    "/questions/",
    "/technology/",
    "/programs/",
    "/sources/",
    "/articles/",
]

LEGACY_NAV_PATTERNS = [
    '<nav class="ref-nav"',
    'aria-label="Explore"',
    'aria-label="Related pages"',
    "ref-nav-label",
]


def load_approved_paths() -> dict[str, dict]:
    """Return map of path → page record for all approved_for_launch pages."""
    path = DATA_DIR / "pages.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {
        p["path"]: p
        for p in data.get("pages", [])
        if p.get("status") == "approved_for_launch"
    }


def extract_locs(xml_text: str) -> list[str]:
    return re.findall(r"<loc>(.+?)</loc>", xml_text)


def url_to_path(url: str) -> str:
    path = url.replace(DOMAIN, "")
    if not path.endswith("/"):
        path += "/"
    return path


def collect_all_page_htmls() -> list[Path]:
    return sorted(PUBLIC_DIR.rglob("index.html"))


def html_path_to_route(html: Path) -> str:
    rel = html.relative_to(PUBLIC_DIR).parent
    route = "/" + str(rel) + "/"
    # Fix root: public/index.html → /./  → /
    route = route.replace("//", "/")
    if route == "/./":
        route = "/"
    # Normalise /./ that can appear for root
    route = re.sub(r"^/\./", "/", route)
    if str(rel) == ".":
        route = "/"
    return route


def run_checks() -> list[str]:
    errors: list[str] = []

    approved = load_approved_paths()
    approved_sitemap_paths = {
        path for path, rec in approved.items() if rec.get("sitemap", True)
    }

    # ── 1. sitemap.xml exists ─────────────────────────────────────────────
    if not SITEMAP_XML.exists():
        errors.append("public/sitemap.xml does not exist")

    # ── 2. sitemap_index.xml exists ───────────────────────────────────────
    if not SITEMAP_INDEX.exists():
        errors.append("public/sitemap_index.xml does not exist")

    # ── 3. sitemap.xml and sitemap_index.xml reference the same sub-sitemaps
    index_refs: list[str] = []
    sitemap_xml_refs: list[str] = []
    if SITEMAP_INDEX.exists() and SITEMAP_XML.exists():
        index_text = SITEMAP_INDEX.read_text(encoding="utf-8")
        xml_text = SITEMAP_XML.read_text(encoding="utf-8")
        index_refs = extract_locs(index_text)
        sitemap_xml_refs = extract_locs(xml_text)
        if set(index_refs) != set(sitemap_xml_refs):
            only_in_index = set(index_refs) - set(sitemap_xml_refs)
            only_in_xml = set(sitemap_xml_refs) - set(index_refs)
            if only_in_index:
                errors.append(
                    f"sitemap_index.xml references not in sitemap.xml: {sorted(only_in_index)}"
                )
            if only_in_xml:
                errors.append(
                    f"sitemap.xml references not in sitemap_index.xml: {sorted(only_in_xml)}"
                )

    # ── 4. All referenced sub-sitemaps physically exist ───────────────────
    for ref in index_refs:
        fname = ref.replace(DOMAIN + "/", "")
        fpath = PUBLIC_DIR / fname
        if not fpath.exists():
            errors.append(f"Sitemap index references missing file: {fname}")

    # ── 5. Collect all sub-sitemap URLs; check count vs generated HTML count
    sitemaps_dir = PUBLIC_DIR / "sitemaps"
    all_sitemap_urls: list[str] = []
    if sitemaps_dir.exists():
        for sm in sorted(sitemaps_dir.glob("*.xml")):
            content = sm.read_text(encoding="utf-8")
            urls = extract_locs(content)
            all_sitemap_urls.extend(urls)

    all_htmls = collect_all_page_htmls()
    generated_count = len(all_htmls)
    sitemap_url_count = len(all_sitemap_urls)

    if sitemap_url_count != generated_count:
        errors.append(
            f"Sitemap URL count ({sitemap_url_count}) does not match generated page count ({generated_count})"
        )

    # ── 6. No duplicate URLs across sitemap files ─────────────────────────
    seen_urls: set[str] = set()
    for url in all_sitemap_urls:
        if url in seen_urls:
            errors.append(f"Duplicate URL in sitemaps: {url}")
        seen_urls.add(url)

    # ── 7. Every sitemap URL resolves to a generated public HTML file ──────
    for url in all_sitemap_urls:
        path = url_to_path(url)
        if path == "/":
            html_path = PUBLIC_DIR / "index.html"
        else:
            html_path = PUBLIC_DIR / path.lstrip("/") / "index.html"
        if not html_path.exists():
            errors.append(f"Sitemap URL has no generated HTML: {url} → {html_path}")

    # ── 8. robots.txt points to the canonical sitemap URL ─────────────────
    if ROBOTS_TXT.exists():
        robots_text = ROBOTS_TXT.read_text(encoding="utf-8")
        sitemap_lines = [
            l.strip() for l in robots_text.splitlines() if l.startswith("Sitemap:")
        ]
        if not sitemap_lines:
            errors.append("robots.txt: no Sitemap directive found")
        else:
            ref = sitemap_lines[0].split(":", 1)[1].strip()
            if ref != CANONICAL_SITEMAP_URL:
                errors.append(
                    f"robots.txt: Sitemap directive points to '{ref}', expected '{CANONICAL_SITEMAP_URL}'"
                )
    else:
        errors.append("public/robots.txt does not exist")

    # ── 9. Every generated HTML page has a canonical URL ──────────────────
    canonical_re = re.compile(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', re.IGNORECASE
    )
    pages_missing_canonical: list[str] = []
    pages_wrong_canonical: list[str] = []

    for html_file in all_htmls:
        content = html_file.read_text(encoding="utf-8")
        route = html_path_to_route(html_file)

        match = canonical_re.search(content)
        if not match:
            pages_missing_canonical.append(route)
            continue

        canonical_href = match.group(1)
        expected = DOMAIN + route
        if canonical_href != expected:
            pages_wrong_canonical.append(
                f"{route}: canonical='{canonical_href}', expected='{expected}'"
            )

    if pages_missing_canonical:
        errors.append(
            f"{len(pages_missing_canonical)} page(s) missing canonical tag: {pages_missing_canonical[:5]}"
        )
    for wrong in pages_wrong_canonical[:10]:
        errors.append(f"Wrong canonical: {wrong}")

    # ── 10. No noindex robots meta on approved public pages ───────────────
    noindex_re = re.compile(
        r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex[^"\']*["\']',
        re.IGNORECASE,
    )
    for html_file in all_htmls:
        route = html_path_to_route(html_file)
        if route not in approved:
            continue
        content = html_file.read_text(encoding="utf-8")
        if noindex_re.search(content):
            errors.append(f"Unexpected noindex robots meta on approved page: {route}")

    # ── 11. All major hubs exist ──────────────────────────────────────────
    for hub_path in REQUIRED_HUBS:
        hub_html = PUBLIC_DIR / hub_path.lstrip("/") / "index.html"
        if not hub_html.exists():
            errors.append(f"Required hub missing: {hub_path}")

    # ── 12. All major hubs contain methodology footer link ─────────────────
    for hub_path in REQUIRED_HUBS:
        hub_html = PUBLIC_DIR / hub_path.lstrip("/") / "index.html"
        if not hub_html.exists():
            continue
        content = hub_html.read_text(encoding="utf-8")
        if 'href="/methodology/"' not in content:
            errors.append(
                f"Hub {hub_path} is missing /methodology/ footer link"
            )
        # /sources/ is the sources hub — skip self-link check; all others must link to /sources/
        if hub_path != "/sources/" and 'href="/sources/"' not in content:
            errors.append(
                f"Hub {hub_path} is missing /sources/ footer link"
            )

    # ── 13. No legacy ref-nav patterns across public/ ─────────────────────
    for html_file in all_htmls:
        content = html_file.read_text(encoding="utf-8")
        route = html_path_to_route(html_file)
        for pattern in LEGACY_NAV_PATTERNS:
            if pattern in content:
                errors.append(
                    f"Legacy ref-nav pattern '{pattern}' found in: {route}"
                )

    # ── 14. No orphan pages outside the approved generation system ─────────
    for html_file in all_htmls:
        route = html_path_to_route(html_file)
        if route not in approved:
            errors.append(
                f"Orphan public page (not in approved_for_launch paths): {route}"
            )

    # ── 15. sitemap URL count sanity: must be > 0 and match approved_sitemap_paths ──
    if sitemap_url_count == 0:
        errors.append("No URLs found in any sitemap file — sitemaps may be empty")

    sitemap_paths_from_urls = {url_to_path(u) for u in all_sitemap_urls}
    missing_from_sitemap = approved_sitemap_paths - sitemap_paths_from_urls
    extra_in_sitemap = sitemap_paths_from_urls - approved_sitemap_paths
    if missing_from_sitemap:
        sample = sorted(missing_from_sitemap)[:5]
        errors.append(
            f"{len(missing_from_sitemap)} approved sitemap page(s) not in any sitemap: {sample}"
        )
    if extra_in_sitemap:
        sample = sorted(extra_in_sitemap)[:5]
        errors.append(
            f"{len(extra_in_sitemap)} sitemap URL(s) not in approved pages: {sample}"
        )

    return errors


def main() -> int:
    print("Indexation Readiness Quality Report")
    print("-" * 40)

    errors = run_checks()

    # Print summary counts
    all_htmls = collect_all_page_htmls()
    sitemaps_dir = PUBLIC_DIR / "sitemaps"
    url_count = 0
    if sitemaps_dir.exists():
        for sm in sitemaps_dir.glob("*.xml"):
            url_count += len(extract_locs(sm.read_text(encoding="utf-8")))

    print(f"  Generated HTML pages: {len(all_htmls)}")
    print(f"  Sitemap URLs total:   {url_count}")
    print(f"  Hubs checked:         {len(REQUIRED_HUBS)}")
    print(f"  Legacy nav patterns:  {len(LEGACY_NAV_PATTERNS)} patterns × {len(all_htmls)} pages")

    if errors:
        print()
        for e in errors:
            print(f"ERROR: {e}")
        print()
        print(f"Indexation readiness: FAIL ({len(errors)} error(s))")
        return 1

    print()
    print("Indexation readiness: PASS")
    print("NOTE: Google Search Console submission remains BLOCKED until explicitly authorized.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
