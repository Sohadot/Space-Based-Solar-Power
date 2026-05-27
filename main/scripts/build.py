#!/usr/bin/env python3
"""Sovereign Generation Engine v1 — Build Script.

Reads approved page registries and data sources, generates public/,
robot.txt, and sitemap files. Blocks any route not approved in pages.json.
"""

import json
import os
import sys
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "main" / "data"
CONTENT_DIR = ROOT / "main" / "content" / "pages"
SCRIPTS_DIR = ROOT / "main" / "scripts"
PUBLIC_DIR = ROOT / "public"
SITEMAPS_DIR = PUBLIC_DIR / "sitemaps"

APPROVED_STATUSES = {"approved_for_launch"}
SITEMAP_BATCH_SIZE = 10_000
DOMAIN = "https://space-based-solar-power.com"


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def approved_pages(pages_data: dict) -> list:
    return [
        p for p in pages_data["pages"]
        if p.get("status") in APPROVED_STATUSES
    ]


def generate_html(page: dict, content: dict | None) -> str:
    title = page.get("title", "")
    description = page.get("description", "")
    path = page.get("path", "/")
    canonical = f"{DOMAIN}{path}"
    h1 = content.get("h1", title) if content else title
    body = content.get("body", "") if content else ""
    internal_links_html = ""
    for link in page.get("requiredInternalLinks", []):
        internal_links_html += f'<li><a href="{link}">{link}</a></li>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="/static/css/main.css">
</head>
<body>
  <header>
    <nav aria-label="Primary navigation">
      <a href="/">Space-Based Solar Power</a>
    </nav>
  </header>
  <main>
    <h1>{h1}</h1>
    <div class="page-body">{body}</div>
    <nav aria-label="Related pages">
      <ul>
{internal_links_html}
      </ul>
    </nav>
  </main>
</body>
</html>"""


def write_page(page: dict, content: dict | None):
    path = page.get("path", "/")
    if path == "/":
        out_path = PUBLIC_DIR / "index.html"
    else:
        slug_path = path.strip("/")
        out_path = PUBLIC_DIR / slug_path / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(generate_html(page, content), encoding="utf-8")
    return str(out_path.relative_to(ROOT))


def load_page_content(page_id: str) -> dict | None:
    candidates = [
        CONTENT_DIR / f"{page_id}.json",
    ]
    for c in candidates:
        if c.exists():
            return load_json(c)
    return None


def generate_sitemap_urls(pages: list) -> list:
    today = date.today().isoformat()
    urls = []
    for p in pages:
        if not p.get("sitemap"):
            continue
        loc = f"{DOMAIN}{p['path']}"
        urls.append({
            "loc": loc,
            "lastmod": today,
            "changefreq": p.get("changefreq", "monthly"),
            "priority": p.get("priority", 0.5),
        })
    return urls


def write_sitemap_file(urls: list, out_path: Path):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{u['loc']}</loc>")
        lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        lines.append(f"    <priority>{u['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def write_sitemap_index(sitemap_files: list):
    today = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for sf in sitemap_files:
        lines.append("  <sitemap>")
        lines.append(f"    <loc>{DOMAIN}/{sf}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append("  </sitemap>")
    lines.append("</sitemapindex>")
    (PUBLIC_DIR / "sitemap_index.xml").write_text("\n".join(lines), encoding="utf-8")


def write_robots(sitemap_ref: str):
    content = f"""User-agent: *
Allow: /
Disallow: /draft/
Disallow: /staging/
Sitemap: {DOMAIN}/{sitemap_ref}
"""
    (PUBLIC_DIR / "robots.txt").write_text(content, encoding="utf-8")


def categorize_pages(pages: list) -> dict:
    categories = {
        "core": [],
        "glossary": [],
        "questions": [],
        "programs": [],
        "countries": [],
        "articles": [],
        "usecases": [],
        "comparisons": [],
        "sources": [],
    }
    for p in pages:
        path = p.get("path", "")
        if path.startswith("/glossary/") and path != "/glossary/":
            categories["glossary"].append(p)
        elif path.startswith("/questions/"):
            categories["questions"].append(p)
        elif path.startswith("/programs/"):
            categories["programs"].append(p)
        elif path.startswith("/countries/"):
            categories["countries"].append(p)
        elif path.startswith("/articles/") and path != "/articles/":
            categories["articles"].append(p)
        elif path.startswith("/use-cases/"):
            categories["usecases"].append(p)
        elif path.startswith("/comparisons/"):
            categories["comparisons"].append(p)
        elif path.startswith("/sources/") and path != "/sources/":
            categories["sources"].append(p)
        else:
            categories["core"].append(p)
    return categories


def build_sitemaps(all_sitemap_urls: list, categories: dict) -> list:
    """Generate sitemap files. Returns list of sitemap relative paths."""
    sitemap_files = []
    today = date.today().isoformat()

    core_urls = generate_sitemap_urls(categories["core"])
    if core_urls:
        sf = SITEMAPS_DIR / "sitemap-core.xml"
        write_sitemap_file(core_urls, sf)
        sitemap_files.append("sitemaps/sitemap-core.xml")

    for cat_name in ["glossary", "questions", "programs", "countries",
                     "articles", "usecases", "comparisons", "sources"]:
        cat_urls = generate_sitemap_urls(categories[cat_name])
        if not cat_urls:
            continue
        batches = [cat_urls[i:i+SITEMAP_BATCH_SIZE]
                   for i in range(0, len(cat_urls), SITEMAP_BATCH_SIZE)]
        for idx, batch in enumerate(batches, start=1):
            fname = f"sitemap-{cat_name}-{idx:03d}.xml"
            sf = SITEMAPS_DIR / fname
            write_sitemap_file(batch, sf)
            sitemap_files.append(f"sitemaps/{fname}")

    return sitemap_files


def main():
    print("Sovereign Generation Engine v1 — Build")
    print("=" * 45)

    pages_data = load_json(DATA_DIR / "pages.json")
    pages = approved_pages(pages_data)
    print(f"Approved pages: {len(pages)}")

    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)
    PUBLIC_DIR.mkdir(parents=True)
    SITEMAPS_DIR.mkdir(parents=True)

    static_css = PUBLIC_DIR / "static" / "css"
    static_css.mkdir(parents=True)
    (static_css / "main.css").write_text(
        "/* main.css — generated placeholder */\nbody { font-family: sans-serif; max-width: 900px; margin: auto; }\n",
        encoding="utf-8"
    )

    generated = []
    for page in pages:
        page_id = page.get("id", "")
        content = load_page_content(page_id)
        out = write_page(page, content)
        generated.append(out)
        print(f"  [GEN] {page.get('path')}")

    all_sitemap_urls = generate_sitemap_urls(pages)
    categories = categorize_pages(pages)
    sitemap_files = build_sitemaps(all_sitemap_urls, categories)

    if len(sitemap_files) > 1:
        write_sitemap_index(sitemap_files)
        sitemap_ref = "sitemap_index.xml"
        print(f"  [SITEMAP] sitemap_index.xml ({len(sitemap_files)} files)")
    else:
        single = sitemap_files[0] if sitemap_files else None
        if single:
            (PUBLIC_DIR / "sitemap.xml").write_text(
                (SITEMAPS_DIR / Path(single).name).read_text(encoding="utf-8"),
                encoding="utf-8"
            )
        sitemap_ref = "sitemap.xml"
        print(f"  [SITEMAP] sitemap.xml ({len(all_sitemap_urls)} URLs)")

    write_robots(sitemap_ref)
    print(f"  [ROBOTS] robots.txt")

    print("\nBuild complete.")
    print(f"Generated: {len(generated)} pages")
    print(f"Sitemap URLs: {len(all_sitemap_urls)}")


if __name__ == "__main__":
    main()
