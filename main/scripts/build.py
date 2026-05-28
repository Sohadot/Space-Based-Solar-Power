#!/usr/bin/env python3
"""Sovereign Generation Engine v1 — Build Script.

Sprint 2: Interface and Reference Launch Correction.
Upgraded templates: home page renders sovereign atlas gateway;
foundation pages use reference section cards;
glossary/question/program pages use governed reference card structure.
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
STATIC_DIR = ROOT / "main" / "static"
PUBLIC_DIR = ROOT / "public"
SITEMAPS_DIR = PUBLIC_DIR / "sitemaps"

APPROVED_STATUSES = {"approved_for_launch"}
SITEMAP_BATCH_SIZE = 10_000
DOMAIN = "https://space-based-solar-power.com"

# Seven core infrastructure layers for the telemetry panel.
# Phase labels represent documented research/program state.
# Do not modify without a DECISION_LOG entry.
TELEMETRY_LAYERS = [
    {"label": "Orbital Core", "value": "Solar Collection Array", "phase": "Research Phase"},
    {"label": "Power Beaming Vector", "value": "Microwave / Laser Transmission", "phase": "Demonstration Phase"},
    {"label": "Rectenna / Terrestrial Reception", "value": "Ground Reception Infrastructure", "phase": "Concept Phase"},
    {"label": "Grid Resilience", "value": "National Energy Infrastructure", "phase": "Strategic Study"},
    {"label": "AI Energy Demand", "value": "High-Density Compute Power", "phase": "Emerging Pressure"},
    {"label": "Defense / Disaster Resilience", "value": "Strategic Power Continuity", "phase": "Strategic Framing"},
    {"label": "Lunar &amp; Space-Industrial", "value": "Off-Earth Infrastructure", "phase": "Concept Phase"},
]

# Primary active constraints shown in the home page constraint matrix preview.
CONSTRAINT_PREVIEW = [
    {"name": "Launch Economics", "status": "Active Constraint"},
    {"name": "Orbital Assembly at Scale", "status": "Active Constraint"},
    {"name": "Wireless Transmission Performance", "status": "Active Constraint"},
    {"name": "Rectenna Deployment Scale", "status": "Active Constraint"},
    {"name": "Safety and Regulatory Acceptance", "status": "Active Constraint"},
]

# Reference atlas card descriptions keyed by path.
REF_ATLAS_DESCS = {
    "/about/": ("Asset Identity", "What this asset is and what it is not."),
    "/methodology/": ("Evaluation Framework", "How claims, sources, and constraints are evaluated."),
    "/framework/": ("Infrastructure Map", "The orbital energy infrastructure chain."),
    "/manifesto/": ("Conceptual Foundation", "Moving energy sovereignty above the atmosphere."),
    "/what-is-space-based-solar-power/": ("Definition", "Foundational definition of the category."),
    "/technology-stack/": ("Technical Reference", "Technical layers of SBSP systems."),
    "/feasibility-and-constraints/": ("Constraint Analysis", "The barriers and unresolved questions."),
    "/strategic-importance/": ("Geopolitical Layer", "Energy sovereignty, AI, defense, and space infrastructure."),
    "/global-programs/": ("Program Registry", "Institutional activity and program tracking."),
    "/tools/": ("Strategic Tools", "Governed tools for decision-support."),
    "/sources/": ("Source Registry", "Institutional, academic, and program-level references."),
    "/articles/": ("Analysis Layer", "Source-disciplined analysis and category commentary."),
    "/glossary/": ("Terminology", "Governed glossary of SBSP and orbital energy terms."),
    "/questions/": ("Reference Questions", "Answered questions with source and answer boundaries."),
    "/programs/": ("Program Profiles", "Detailed profiles of institutional SBSP programs."),
}


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


def _path_to_label(path: str) -> str:
    slug = path.strip("/").split("/")[-1] if path.strip("/") else ""
    return slug.replace("-", " ").title() if slug else "Home"


def _link_chip(path: str, label: str) -> str:
    return f'<a class="link-chip" href="{path}">{_escape_html(label)}</a>'


def _page_shell(page: dict, h1: str, body: str) -> str:
    title = page.get("title", "")
    description = page.get("description", "")
    path = page.get("path", "/")
    canonical = f"{DOMAIN}{path}"
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
  <header class="site-header">
    <nav class="site-nav" aria-label="Primary navigation">
      <a class="home-link" href="/">Space-Based Solar Power</a>
      <div class="mission-status" aria-label="Site status">
        <span class="mission-status-dot" aria-hidden="true"></span>
        <span>Reference Active</span>
      </div>
    </nav>
  </header>
  <main class="page-container">
    <h1>{_escape_html(h1)}</h1>
    {body}
  </main>
</body>
</html>"""


def _render_hub_source_footer() -> str:
    return (
        '<div class="hub-source-links">'
        '<span class="hub-source-label">Source &amp; methodology</span>'
        '<a class="link-chip" href="/methodology/">Methodology</a>'
        '<a class="link-chip" href="/sources/">Sources</a>'
        '</div>'
    )


def render_content_sections_html(sections: list, approved_paths: set) -> str:
    """Render content sections as plain sections (fallback for pages without structured sections)."""
    html_parts = []
    for section in sections:
        heading = _escape_html(section.get("heading", ""))
        body_paras = section.get("body", [])
        links = section.get("links", [])

        parts = ['<section class="page-section">']
        if heading:
            parts.append(f'  <h2>{heading}</h2>')
        for para in body_paras:
            parts.append(f'  <p>{_escape_html(para)}</p>')
        visible_links = [lk for lk in links if lk.get("path") in approved_paths]
        if visible_links:
            parts.append('  <div class="section-links">')
            for lk in visible_links:
                label = _escape_html(lk.get("label", lk.get("path", "")))
                parts.append(f'    <a href="{lk["path"]}">{label}</a>')
            parts.append('  </div>')
        parts.append('</section>')
        html_parts.append("\n".join(parts))
    return "\n".join(html_parts)


def render_reference_cards_html(sections: list, approved_paths: set) -> str:
    """Render content sections as governed reference section cards."""
    html_parts = []
    for section in sections:
        heading = _escape_html(section.get("heading", ""))
        body_paras = section.get("body", [])
        links = section.get("links", [])

        parts = ['<div class="reference-section">']
        if heading:
            parts.append('  <div class="reference-section-header">')
            parts.append(f'    <h2>{heading}</h2>')
            parts.append('  </div>')
        parts.append('  <div class="reference-section-body">')
        for para in body_paras:
            parts.append(f'    <p>{_escape_html(para)}</p>')
        parts.append('  </div>')
        visible_links = [lk for lk in links if lk.get("path") in approved_paths]
        if visible_links:
            parts.append('  <div class="reference-section-links">')
            for lk in visible_links:
                label = _escape_html(lk.get("label", lk.get("path", "")))
                parts.append(f'    {_link_chip(lk["path"], lk.get("label", lk.get("path", "")))}')
            parts.append('  </div>')
        parts.append('</div>')
        html_parts.append("\n".join(parts))
    return "\n".join(html_parts)


def _render_telemetry_panel() -> str:
    parts = ['<div class="telemetry-panel" aria-label="Infrastructure system layers">']
    for layer in TELEMETRY_LAYERS:
        parts.append('  <div class="telemetry-card">')
        parts.append(f'    <p class="telemetry-card-label">{layer["label"]}</p>')
        parts.append(f'    <p class="telemetry-card-value">{layer["value"]}</p>')
        parts.append(f'    <p class="telemetry-card-phase">{layer["phase"]}</p>')
        parts.append('  </div>')
    parts.append('</div>')
    return "\n".join(parts)


def _render_ref_atlas_grid(internal_links: list, approved_paths: set) -> str:
    parts = ['<nav class="ref-atlas-nav" aria-label="Reference atlas navigation">']
    parts.append('  <p class="ref-atlas-nav-label">Reference Atlas</p>')
    parts.append('  <div class="ref-atlas-grid">')
    for lk in internal_links:
        lpath = lk.get("path", "")
        if lpath not in approved_paths:
            continue
        label = lk.get("label", _path_to_label(lpath))
        cat, desc = REF_ATLAS_DESCS.get(lpath, ("", ""))
        parts.append(f'    <a href="{lpath}" class="ref-atlas-card">')
        if cat:
            parts.append(f'      <p class="ref-atlas-card-label">{_escape_html(cat)}</p>')
        parts.append(f'      <p class="ref-atlas-card-title">{_escape_html(label)}</p>')
        if desc:
            parts.append(f'      <p class="ref-atlas-card-desc">{_escape_html(desc)}</p>')
        parts.append('    </a>')
    parts.append('  </div>')
    parts.append('</nav>')
    return "\n".join(parts)


def _render_constraint_preview(approved_paths: set) -> str:
    constraint_link = "/feasibility-and-constraints/"
    has_link = constraint_link in approved_paths
    parts = ['<div class="constraint-matrix-preview">']
    parts.append('  <div class="constraint-matrix-header">')
    parts.append('    <span class="constraint-matrix-title">Orbital Energy Constraint Matrix — Preview</span>')
    if has_link:
        parts.append(f'    <a href="{constraint_link}" class="constraint-matrix-link">Full analysis</a>')
    parts.append('  </div>')
    for c in CONSTRAINT_PREVIEW:
        parts.append('  <div class="constraint-row">')
        parts.append(f'    <span class="constraint-name">{_escape_html(c["name"])}</span>')
        parts.append(f'    <span class="constraint-status">{_escape_html(c["status"])}</span>')
        parts.append('  </div>')
    parts.append('</div>')
    return "\n".join(parts)


def _render_source_trust_block(approved_paths: set) -> str:
    methodology_link = "/methodology/"
    sources_link = "/sources/"
    parts = ['<div class="source-trust-block">']
    parts.append('  <p class="source-trust-label">Source &amp; Methodology Posture</p>')
    parts.append('  <p class="source-trust-desc">All claims on this site are tied to verifiable institutional, academic, or program-level sources. Technical and economic claims are qualified with defined boundaries. The asset distinguishes between source-verified facts, institutional summaries, conceptual framing, and unresolved scenarios.</p>')
    links = []
    if methodology_link in approved_paths:
        links.append(f'<a href="{methodology_link}">Read the methodology</a>')
    if sources_link in approved_paths:
        links.append(f'<a href="{sources_link}">Source registry</a>')
    if links:
        parts.append('  <div class="source-trust-links">')
        for lnk in links:
            parts.append(f'    {lnk}')
        parts.append('  </div>')
    parts.append('</div>')
    return "\n".join(parts)


def generate_home_html(page: dict, content: dict, approved_paths: set) -> str:
    hero = content.get("hero", {})
    sections = content.get("sections", [])
    internal_links = content.get("internalLinks", [])
    h1 = content.get("h1", page.get("title", ""))

    eyebrow = _escape_html(hero.get("eyebrow", ""))
    hero_title = _escape_html(hero.get("title", ""))
    subtitle = _escape_html(hero.get("subtitle", ""))
    thesis = _escape_html(hero.get("thesis", ""))

    hero_parts = ['<div class="orbital-atlas-hero">']
    if eyebrow:
        hero_parts.append(f'  <p class="hero-eyebrow">{eyebrow}</p>')
    if hero_title:
        hero_parts.append(f'  <p class="hero-title">{hero_title}</p>')
    if subtitle:
        hero_parts.append(f'  <p class="hero-subtitle">{subtitle}</p>')
    if thesis:
        hero_parts.append(f'  <blockquote class="hero-thesis">{thesis}</blockquote>')
    hero_parts.append('</div>')
    hero_html = "\n".join(hero_parts)

    telemetry_html = _render_telemetry_panel()
    atlas_html = _render_ref_atlas_grid(internal_links, approved_paths)
    constraint_html = _render_constraint_preview(approved_paths)
    trust_html = _render_source_trust_block(approved_paths)
    sections_html = render_content_sections_html(sections, approved_paths)

    title = _escape_html(page.get("title", ""))
    description = _escape_html(page.get("description", ""))
    canonical = f"{DOMAIN}{page.get('path', '/')}"
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
  <header class="site-header">
    <nav class="site-nav" aria-label="Primary navigation">
      <a class="home-link" href="/">Space-Based Solar Power</a>
      <div class="mission-status" aria-label="Site status">
        <span class="mission-status-dot" aria-hidden="true"></span>
        <span>Reference Active</span>
      </div>
    </nav>
  </header>
  <main class="page-container">
    <h1>{_escape_html(h1)}</h1>
    {hero_html}
    {telemetry_html}
    {atlas_html}
    {constraint_html}
    {trust_html}
    {sections_html}
  </main>
</body>
</html>"""


def generate_glossary_term_html(term: dict, page: dict) -> str:
    h1 = term.get("term", page["title"])
    short = _escape_html(term.get("shortDefinition", ""))
    definition = _escape_html(term.get("definition", ""))
    claim = _escape_html(term.get("claimBoundary", ""))
    internal_links = page.get("requiredInternalLinks", [])

    parts = ['<div class="reference-card">']
    parts.append('  <div class="reference-card-type">Glossary Term</div>')
    parts.append('  <div class="reference-card-body">')
    if short:
        parts.append(f'    <p class="reference-card-short">{short}</p>')
    if definition:
        parts.append(f'    <div class="reference-card-full"><p>{definition}</p></div>')
    parts.append('  </div>')
    if claim:
        parts.append('  <div class="reference-card-boundary">')
        parts.append('    <p class="reference-card-boundary-label">Claim Boundary</p>')
        parts.append(f'    <p class="reference-card-boundary-text">{claim}</p>')
        parts.append('  </div>')
    if internal_links:
        parts.append('  <div class="reference-card-links">')
        for lk in internal_links:
            parts.append(f'    {_link_chip(lk, _path_to_label(lk))}')
        parts.append('  </div>')
    parts.append('  <div class="reference-card-source-links">')
    parts.append('    <span class="reference-card-source-label">Source &amp; methodology</span>')
    parts.append('    <a class="link-chip" href="/methodology/">Methodology</a>')
    parts.append('    <a class="link-chip" href="/sources/">Sources</a>')
    parts.append('  </div>')
    parts.append('</div>')
    body = "\n".join(parts)
    return _page_shell(page, h1, body)


def generate_question_html(question: dict, page: dict) -> str:
    h1 = question.get("question", page["title"])
    answer = _escape_html(question.get("answer", ""))
    boundary = _escape_html(question.get("answerBoundary", ""))
    internal_links = page.get("requiredInternalLinks", [])

    parts = ['<div class="reference-card">']
    parts.append('  <div class="reference-card-type">Reference Question</div>')
    parts.append('  <div class="reference-card-body">')
    if answer:
        parts.append(f'    <div class="reference-card-full"><p>{answer}</p></div>')
    parts.append('  </div>')
    if boundary:
        parts.append('  <div class="reference-card-boundary">')
        parts.append('    <p class="reference-card-boundary-label">Answer Boundary</p>')
        parts.append(f'    <p class="reference-card-boundary-text">{boundary}</p>')
        parts.append('  </div>')
    if internal_links:
        parts.append('  <div class="reference-card-links">')
        for lk in internal_links:
            parts.append(f'    {_link_chip(lk, _path_to_label(lk))}')
        parts.append('  </div>')
    parts.append('  <div class="reference-card-source-links">')
    parts.append('    <span class="reference-card-source-label">Source &amp; methodology</span>')
    parts.append('    <a class="link-chip" href="/methodology/">Methodology</a>')
    parts.append('    <a class="link-chip" href="/sources/">Sources</a>')
    parts.append('  </div>')
    parts.append('</div>')
    body = "\n".join(parts)
    return _page_shell(page, h1, body)


def generate_program_html(program: dict, page: dict) -> str:
    h1 = program.get("programName", page["title"])
    institution = _escape_html(program.get("institution", ""))
    country = _escape_html(program.get("country", ""))
    start_year = program.get("startYear", "")
    status = _escape_html(program.get("status", "").replace("_", " "))
    description = _escape_html(program.get("description", ""))
    claim = _escape_html(program.get("claimBoundary", ""))
    internal_links = page.get("requiredInternalLinks", [])

    meta_rows = []
    if institution:
        meta_rows.append(f'<dt>Institution</dt><dd>{institution}</dd>')
    if country:
        meta_rows.append(f'<dt>Country</dt><dd>{country}</dd>')
    if start_year:
        meta_rows.append(f'<dt>Start year</dt><dd>{start_year}</dd>')
    if status:
        meta_rows.append(f'<dt>Status</dt><dd>{status}</dd>')

    parts = ['<div class="reference-card">']
    parts.append('  <div class="reference-card-type">Program Profile</div>')
    if meta_rows:
        parts.append('  <dl class="program-meta">' + "".join(meta_rows) + '</dl>')
    parts.append('  <div class="reference-card-body">')
    if description:
        parts.append(f'    <div class="reference-card-full"><p>{description}</p></div>')
    parts.append('  </div>')
    if claim:
        parts.append('  <div class="reference-card-boundary">')
        parts.append('    <p class="reference-card-boundary-label">Claim Boundary</p>')
        parts.append(f'    <p class="reference-card-boundary-text">{claim}</p>')
        parts.append('  </div>')
    if internal_links:
        parts.append('  <div class="reference-card-links">')
        for lk in internal_links:
            parts.append(f'    {_link_chip(lk, _path_to_label(lk))}')
        parts.append('  </div>')
    parts.append('  <div class="reference-card-source-links">')
    parts.append('    <span class="reference-card-source-label">Source &amp; methodology</span>')
    parts.append('    <a class="link-chip" href="/methodology/">Methodology</a>')
    parts.append('    <a class="link-chip" href="/sources/">Sources</a>')
    parts.append('  </div>')
    parts.append('</div>')
    body = "\n".join(parts)
    return _page_shell(page, h1, body)


def generate_glossary_hub_html(page: dict, seed_data: dict, trial_manifest: dict | None) -> str:
    h1 = page.get("title", "SBSP Glossary")
    description = _escape_html(page.get("description", ""))
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
    intro = f'<p class="hub-intro">{description}</p>\n' if description else ""
    body = (intro
            + f'<ul class="glossary-index">\n{list_html}\n    </ul>\n'
            + _render_hub_source_footer())
    return _page_shell(page, h1, body)


def generate_questions_hub_html(page: dict, seed_data: dict, trial_manifest: dict | None) -> str:
    h1 = page.get("title", "SBSP Questions")
    description = _escape_html(page.get("description", ""))
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
    intro = f'<p class="hub-intro">{description}</p>\n' if description else ""
    body = (intro
            + f'<ul class="questions-index">\n{list_html}\n    </ul>\n'
            + _render_hub_source_footer())
    return _page_shell(page, h1, body)


def generate_programs_hub_html(page: dict, seed_data: dict, trial_manifest: dict | None) -> str:
    h1 = page.get("title", "SBSP Program Profiles")
    description = _escape_html(page.get("description", ""))
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
    intro = f'<p class="hub-intro">{description}</p>\n' if description else ""
    body = (intro
            + f'<ul class="programs-index">\n{list_html}\n    </ul>\n'
            + _render_hub_source_footer())
    return _page_shell(page, h1, body)


def generate_html(page: dict, content: dict | None,
                  approved_paths: set | None = None) -> str:
    if approved_paths is None:
        approved_paths = set()
    title = page.get("title", "")
    h1 = content.get("h1", title) if content else title
    if content and content.get("sections"):
        body = render_reference_cards_html(content["sections"], approved_paths)
    else:
        body = content.get("body", "") if content else ""
    return _page_shell(page, h1, body)


def write_page(page: dict, content: dict | None,
               seed_data: dict | None = None,
               trial_manifest: dict | None = None,
               approved_paths: set | None = None):
    if approved_paths is None:
        approved_paths = set()
    path = page.get("path", "/")
    if path == "/":
        out_path = PUBLIC_DIR / "index.html"
    else:
        slug_path = path.strip("/")
        out_path = PUBLIC_DIR / slug_path / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    seed_source = page.get("seedSource")
    seed_id = page.get("seedId")

    # Try content by slug as fallback when ID does not match the content filename.
    if content is None:
        page_slug = page.get("slug", "")
        page_id_val = page.get("id", "")
        if page_slug and page_slug != page_id_val:
            content = load_page_content(page_slug)

    if seed_data and seed_source == "glossary_term" and seed_id:
        term = seed_data["glossary"].get(seed_id)
        html = generate_glossary_term_html(term, page) if term else generate_html(page, content, approved_paths)
    elif seed_data and seed_source == "question" and seed_id:
        question = seed_data["questions"].get(seed_id)
        html = generate_question_html(question, page) if question else generate_html(page, content, approved_paths)
    elif seed_data and seed_source == "program" and seed_id:
        program = seed_data["programs"].get(seed_id)
        html = generate_program_html(program, page) if program else generate_html(page, content, approved_paths)
    elif seed_data and seed_source == "glossary_hub":
        html = generate_glossary_hub_html(page, seed_data, trial_manifest)
    elif seed_data and seed_source == "questions_hub":
        html = generate_questions_hub_html(page, seed_data, trial_manifest)
    elif seed_data and seed_source == "programs_hub":
        html = generate_programs_hub_html(page, seed_data, trial_manifest)
    elif content and content.get("hero"):
        html = generate_home_html(page, content, approved_paths)
    else:
        html = generate_html(page, content, approved_paths)

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


def write_sitemap_index(sitemap_files: list, out_path: Path | None = None):
    if out_path is None:
        out_path = PUBLIC_DIR / "sitemap_index.xml"
    today = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for sf in sitemap_files:
        lines.append("  <sitemap>")
        lines.append(f"    <loc>{DOMAIN}/{sf}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append("  </sitemap>")
    lines.append("</sitemapindex>")
    out_path.write_text("\n".join(lines), encoding="utf-8")


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
    source_css = STATIC_DIR / "css" / "main.css"
    if source_css.exists():
        shutil.copy2(source_css, static_css / "main.css")
        print("  [CSS] main/static/css/main.css → public/static/css/main.css")
    else:
        print("  [WARN] main/static/css/main.css not found — writing placeholder")
        (static_css / "main.css").write_text(
            "/* main.css — placeholder */\nbody { font-family: sans-serif; max-width: 900px; margin: auto; }\n",
            encoding="utf-8"
        )

    approved_paths = {p["path"] for p in pages}

    generated = []
    for page in pages:
        page_id = page.get("id", "")
        content = load_page_content(page_id)
        out = write_page(page, content, seed_data=seed_data,
                         trial_manifest=trial_manifest, approved_paths=approved_paths)
        generated.append(out)
        print(f"  [GEN] {page.get('path')}")

    all_sitemap_urls = generate_sitemap_urls(pages)
    categories = categorize_pages(pages)
    sitemap_files = build_sitemaps(all_sitemap_urls, categories)

    if len(sitemap_files) > 1:
        write_sitemap_index(sitemap_files, PUBLIC_DIR / "sitemap.xml")
        write_sitemap_index(sitemap_files, PUBLIC_DIR / "sitemap_index.xml")
        print(f"  [SITEMAP] sitemap.xml (index, {len(sitemap_files)} files)")
    else:
        single = sitemap_files[0] if sitemap_files else None
        if single:
            (PUBLIC_DIR / "sitemap.xml").write_text(
                (SITEMAPS_DIR / Path(single).name).read_text(encoding="utf-8"),
                encoding="utf-8"
            )
        print(f"  [SITEMAP] sitemap.xml ({len(all_sitemap_urls)} URLs)")

    write_robots("sitemap.xml")
    print(f"  [ROBOTS] robots.txt")

    (PUBLIC_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print(f"  [NOJEKYLL] .nojekyll")

    print("\nBuild complete.")
    print(f"Generated: {len(generated)} pages")
    print(f"Sitemap URLs: {len(all_sitemap_urls)}")


if __name__ == "__main__":
    main()
