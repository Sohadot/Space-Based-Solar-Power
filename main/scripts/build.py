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


def load_seed_data() -> dict:
    """Load all seed data files keyed by ID for fast lookup."""
    seed = {"glossary": {}, "questions": {}, "programs": {}}

    glossary_path = DATA_DIR / "glossary_terms.json"
    if glossary_path.exists():
        data = load_json(glossary_path)
        terms = data if isinstance(data, list) else data.get("terms", [])
        for t in terms:
            seed["glossary"][t["id"]] = t

    questions_path = DATA_DIR / "question_bank.json"
    if questions_path.exists():
        data = load_json(questions_path)
        questions = data if isinstance(data, list) else data.get("questions", [])
        for q in questions:
            seed["questions"][q["id"]] = q

    programs_path = DATA_DIR / "program_registry.json"
    if programs_path.exists():
        data = load_json(programs_path)
        programs = data if isinstance(data, list) else data.get("programs", [])
        for p in programs:
            seed["programs"][p["id"]] = p

    return seed


def load_trial_manifest() -> dict | None:
    path = DATA_DIR / "publication_trial_v1a.json"
    if path.exists():
        return load_json(path)
    return None


def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )


def _build_nav_links(links: list) -> str:
    parts = []
    for link in links:
        parts.append(f'        <li><a href="{link}">{link}</a></li>')
    return "\n".join(parts)


def _page_shell(page: dict, h1: str, body: str) -> str:
    title = page.get("title", "")
    description = page.get("description", "")
    path = page.get("path", "/")
    canonical = f"{DOMAIN}{path}"
    nav_links = _build_nav_links(page.get("requiredInternalLinks", []))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{_escape_html(title)}</title>
  <meta name="description" content="{_escape_html(description)}">
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
    <h1>{_escape_html(h1)}</h1>
    <div class="page-body">{body}</div>
    <nav aria-label="Related pages">
      <ul>
{nav_links}
      </ul>
    </nav>
  </main>
</body>
</html>"""


def generate_glossary_term_html(term: dict, page: dict) -> str:
    h1 = term.get("term", page["title"])
    short = _escape_html(term.get("shortDefinition", ""))
    definition = _escape_html(term.get("definition", ""))
    claim = _escape_html(term.get("claimBoundary", ""))
    body = f'<p class="short-definition">{short}</p>\n'
    body += f'<div class="definition"><p>{definition}</p></div>\n'
    if claim:
        body += f'<aside class="claim-boundary"><strong>Claim boundary:</strong> {claim}</aside>\n'
    return _page_shell(page, h1, body)


def generate_question_html(question: dict, page: dict) -> str:
    h1 = question.get("question", page["title"])
    answer = _escape_html(question.get("answer", ""))
    boundary = _escape_html(question.get("answerBoundary", ""))
    body = f'<div class="answer"><p>{answer}</p></div>\n'
    if boundary:
        body += f'<aside class="answer-boundary"><strong>Answer boundary:</strong> {boundary}</aside>\n'
    return _page_shell(page, h1, body)


def generate_program_html(program: dict, page: dict) -> str:
    h1 = program.get("programName", page["title"])
    institution = _escape_html(program.get("institution", ""))
    country = _escape_html(program.get("country", ""))
    start_year = program.get("startYear", "")
    status = _escape_html(program.get("status", "").replace("_", " "))
    description = _escape_html(program.get("description", ""))
    claim = _escape_html(program.get("claimBoundary", ""))

    meta = []
    if institution:
        meta.append(f'<dt>Institution</dt><dd>{institution}</dd>')
    if country:
        meta.append(f'<dt>Country</dt><dd>{country}</dd>')
    if start_year:
        meta.append(f'<dt>Start year</dt><dd>{start_year}</dd>')
    if status:
        meta.append(f'<dt>Status</dt><dd>{status}</dd>')

    body = f'<dl class="program-meta">{"".join(meta)}</dl>\n'
    body += f'<div class="program-description"><p>{description}</p></div>\n'
    if claim:
        body += f'<aside class="claim-boundary"><strong>Claim boundary:</strong> {claim}</aside>\n'
    return _page_shell(page, h1, body)


def generate_glossary_hub_html(page: dict, seed_data: dict, trial_manifest: dict | None) -> str:
    h1 = page.get("title", "SBSP Glossary")
    term_ids = (trial_manifest or {}).get("glossaryTerms", [])
    items = []
    for tid in term_ids:
        term = seed_data["glossary"].get(tid)
        if not term:
            continue
        t_path = term.get("path", f"/glossary/{term.get('slug', tid)}/")
        t_name = _escape_html(term.get("term", tid))
        t_short = _escape_html(term.get("shortDefinition", ""))
        items.append(
            f'<li><a href="{t_path}">{t_name}</a>'
            + (f' — {t_short}' if t_short else '')
            + '</li>'
        )
    list_html = "\n".join(f"      {item}" for item in items)
    body = f'<ul class="glossary-index">\n{list_html}\n    </ul>\n'
    return _page_shell(page, h1, body)


def generate_questions_hub_html(page: dict, seed_data: dict, trial_manifest: dict | None) -> str:
    h1 = page.get("title", "SBSP Questions")
    question_ids = (trial_manifest or {}).get("questions", [])
    items = []
    for qid in question_ids:
        q = seed_data["questions"].get(qid)
        if not q:
            continue
        q_path = q.get("path", f"/questions/{q.get('slug', qid)}/")
        q_text = _escape_html(q.get("question", qid))
        items.append(f'<li><a href="{q_path}">{q_text}</a></li>')
    list_html = "\n".join(f"      {item}" for item in items)
    body = f'<ul class="questions-index">\n{list_html}\n    </ul>\n'
    return _page_shell(page, h1, body)


def generate_programs_hub_html(page: dict, seed_data: dict, trial_manifest: dict | None) -> str:
    h1 = page.get("title", "SBSP Program Profiles")
    program_ids = (trial_manifest or {}).get("programs", [])
    items = []
    for pid in program_ids:
        prog = seed_data["programs"].get(pid)
        if not prog:
            continue
        p_path = prog.get("path", f"/programs/{prog.get('slug', pid)}/")
        p_name = _escape_html(prog.get("programName", pid))
        p_inst = _escape_html(prog.get("institution", ""))
        items.append(
            f'<li><a href="{p_path}">{p_name}</a>'
            + (f' — {p_inst}' if p_inst else '')
            + '</li>'
        )
    list_html = "\n".join(f"      {item}" for item in items)
    body = f'<ul class="programs-index">\n{list_html}\n    </ul>\n'
    return _page_shell(page, h1, body)


def generate_html(page: dict, content: dict | None) -> str:
    title = page.get("title", "")
    h1 = content.get("h1", title) if content else title
    body = content.get("body", "") if content else ""
    return _page_shell(page, h1, body)


def write_page(page: dict, content: dict | None,
               seed_data: dict | None = None,
               trial_manifest: dict | None = None):
    path = page.get("path", "/")
    if path == "/":
        out_path = PUBLIC_DIR / "index.html"
    else:
        slug_path = path.strip("/")
        out_path = PUBLIC_DIR / slug_path / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    seed_source = page.get("seedSource")
    seed_id = page.get("seedId")

    if seed_data and seed_source == "glossary_term" and seed_id:
        term = seed_data["glossary"].get(seed_id)
        html = generate_glossary_term_html(term, page) if term else generate_html(page, content)
    elif seed_data and seed_source == "question" and seed_id:
        question = seed_data["questions"].get(seed_id)
        html = generate_question_html(question, page) if question else generate_html(page, content)
    elif seed_data and seed_source == "program" and seed_id:
        program = seed_data["programs"].get(seed_id)
        html = generate_program_html(program, page) if program else generate_html(page, content)
    elif seed_data and seed_source == "glossary_hub":
        html = generate_glossary_hub_html(page, seed_data, trial_manifest)
    elif seed_data and seed_source == "questions_hub":
        html = generate_questions_hub_html(page, seed_data, trial_manifest)
    elif seed_data and seed_source == "programs_hub":
        html = generate_programs_hub_html(page, seed_data, trial_manifest)
    else:
        html = generate_html(page, content)

    out_path.write_text(html, encoding="utf-8")
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

    seed_data = load_seed_data()
    trial_manifest = load_trial_manifest()
    if trial_manifest:
        print(f"Trial manifest: {trial_manifest.get('phase', 'unknown')} "
              f"({trial_manifest.get('totalPages', '?')} pages)")

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
        out = write_page(page, content, seed_data=seed_data, trial_manifest=trial_manifest)
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

    (PUBLIC_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print(f"  [NOJEKYLL] .nojekyll")

    print("\nBuild complete.")
    print(f"Generated: {len(generated)} pages")
    print(f"Sitemap URLs: {len(all_sitemap_urls)}")


if __name__ == "__main__":
    main()
