#!/usr/bin/env python3
"""Sitemap Validator — ensures sitemaps contain only approved, published URLs."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "main" / "data"
PUBLIC_DIR = ROOT / "public"

ERRORS = []
MAX_SITEMAP_URLS = 50_000
DOMAIN = "https://space-based-solar-power.com"


def error(msg: str):
    ERRORS.append(msg)
    print(f"  [FAIL] {msg}")


def load_approved_paths() -> set:
    import json
    pages_path = DATA_DIR / "pages.json"
    if not pages_path.exists():
        return set()
    with open(pages_path, encoding="utf-8") as f:
        data = json.load(f)
    return {
        p["path"]
        for p in data.get("pages", [])
        if p.get("status") == "approved_for_launch" and p.get("sitemap")
    }


def extract_urls_from_sitemap(content: str) -> list:
    return re.findall(r"<loc>(.+?)</loc>", content)


def validate_sitemap_file(sitemap_path: Path, approved_paths: set):
    if not sitemap_path.exists():
        return
    content = sitemap_path.read_text(encoding="utf-8")
    urls = extract_urls_from_sitemap(content)

    if len(urls) > MAX_SITEMAP_URLS:
        error(f"{sitemap_path.name}: exceeds {MAX_SITEMAP_URLS} URLs ({len(urls)} found)")

    for url in urls:
        path = url.replace(DOMAIN, "")
        if not path.endswith("/"):
            path += "/"
        if path not in approved_paths and approved_paths:
            error(f"{sitemap_path.name}: URL '{url}' not in approved sitemap pages")


def validate_sitemap_index():
    index_path = PUBLIC_DIR / "sitemap_index.xml"
    if not index_path.exists():
        return
    content = index_path.read_text(encoding="utf-8")
    refs = re.findall(r"<loc>(.+?)</loc>", content)
    for ref in refs:
        fname = ref.replace(DOMAIN + "/", "")
        file_path = PUBLIC_DIR / fname
        if not file_path.exists():
            error(f"sitemap_index.xml references non-existent file: '{fname}'")


def validate_robots_sitemap_ref():
    robots = PUBLIC_DIR / "robots.txt"
    if not robots.exists():
        return
    content = robots.read_text(encoding="utf-8")
    sitemap_lines = [l for l in content.splitlines() if l.startswith("Sitemap:")]
    if not sitemap_lines:
        error("robots.txt: no Sitemap directive found")
        return
    for line in sitemap_lines:
        ref = line.split(":", 1)[1].strip()
        fname = ref.replace(DOMAIN + "/", "")
        if not (PUBLIC_DIR / fname).exists():
            error(f"robots.txt: Sitemap reference '{fname}' does not exist")


def is_sitemap_index(content: str) -> bool:
    return "<sitemapindex" in content


def validate_sitemap_xml_exists():
    if not (PUBLIC_DIR / "sitemap.xml").exists():
        error("public/sitemap.xml does not exist — canonical sitemap entry point is missing")


def validate_sitemap_xml_index_refs(content: str):
    """When sitemap.xml is a sitemap index, validate that referenced files exist."""
    refs = re.findall(r"<loc>(.+?)</loc>", content)
    for ref in refs:
        fname = ref.replace(DOMAIN + "/", "")
        file_path = PUBLIC_DIR / fname
        if not file_path.exists():
            error(f"sitemap.xml (index): references non-existent file '{fname}'")


def main() -> int:
    print("validate_sitemap.py")
    print("-" * 40)
    approved_paths = load_approved_paths()

    validate_sitemap_xml_exists()

    sitemap_xml = PUBLIC_DIR / "sitemap.xml"
    if sitemap_xml.exists():
        content = sitemap_xml.read_text(encoding="utf-8")
        if is_sitemap_index(content):
            validate_sitemap_xml_index_refs(content)
        else:
            validate_sitemap_file(sitemap_xml, approved_paths)

    sitemaps_dir = PUBLIC_DIR / "sitemaps"
    if sitemaps_dir.exists():
        for sm in sitemaps_dir.glob("*.xml"):
            validate_sitemap_file(sm, approved_paths)

    validate_sitemap_index()
    validate_robots_sitemap_ref()

    if ERRORS:
        print(f"\nSitemap validation: {len(ERRORS)} error(s) found.")
        return 1
    print("Sitemap validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
