#!/usr/bin/env python3
"""Sovereign Generation Engine v1 — Build Script.

Sprint 2: Interface and Reference Launch Correction.
Upgraded templates: home page renders sovereign atlas gateway;
foundation pages use reference section cards;
glossary/question/program pages use governed reference card structure.
Sprint v1B-D: Program hub upgraded with cluster grouping, status panel,
expansion note, and richer program profile rendering.
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

TELEMETRY_LAYERS = [
    {"label": "Orbital Core", "value": "Solar Collection Array", "phase": "Research Phase"},
    {"label": "Power Beaming Vector", "value": "Microwave / Laser Transmission", "phase": "Demonstration Phase"},
    {"label": "Rectenna / Terrestrial Reception", "value": "Ground Reception Infrastructure", "phase": "Concept Phase"},
    {"label": "Grid Resilience", "value": "National Energy Infrastructure", "phase": "Strategic Study"},
    {"label": "AI Energy Demand", "value": "High-Density Compute Power", "phase": "Emerging Pressure"},
    {"label": "Defense / Disaster Resilience", "value": "Strategic Power Continuity", "phase": "Strategic Framing"},
    {"label": "Lunar &amp; Space-Industrial", "value": "Off-Earth Infrastructure", "phase": "Concept Phase"},
]

CONSTRAINT_PREVIEW = [
    {"name": "Launch Economics", "status": "Active Constraint"},
    {"name": "Orbital Assembly at Scale", "status": "Active Constraint"},
    {"name": "Wireless Transmission Performance", "status": "Active Constraint"},
    {"name": "Rectenna Deployment Scale", "status": "Active Constraint"},
    {"name": "Safety and Regulatory Acceptance", "status": "Active Constraint"},
]

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
    seed = {"glossary": {}, "questions": {}, "programs": {}, "technology": {}, "question_paths": {}}

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

    # v1B-D: also load program_pages.json — overrides/extends program_registry entries
    program_pages_path = DATA_DIR / "program_pages.json"
    if program_pages_path.exists():
        data = load_json(program_pages_path)
        prog_pages = data if isinstance(data, list) else data.get("programs", [])
        for p in prog_pages:
            seed["programs"][p["id"]] = p

    technology_path = DATA_DIR / "technology_pages.json"
    if technology_path.exists():
        data = load_json(technology_path)
        tech_pages = data if isinstance(data, list) else data.get("pages", [])
        for t in tech_pages:
            seed["technology"][t["id"]] = t

    # v1B-D: build question ID → actual page path lookup from pages.json
    pages_path = DATA_DIR / "pages.json"
    if pages_path.exists():
        data = load_json(pages_path)
        for p in data.get("pages", []):
            if p.get("type") == "question_answer" and p.get("seedId") and p.get("path"):
                seed["question_paths"][p["seedId"]] = p["path"]

    # v1B-E: load governed source registry
    seed["sources"] = []
    source_registry_path = DATA_DIR / "source_registry.json"
    if source_registry_path.exists():
        data = load_json(source_registry_path)
        seed["sources"] = data if isinstance(data, list) else data.get("sources", [])

    return seed


CLUSTER_ORDER = [
    ("core-infrastructure", "Core Infrastructure"),
    ("transmission-reception", "Transmission and Reception"),
    ("grid-energy-systems", "Grid and Energy Systems"),
    ("constraints-governance", "Constraints and Governance"),
    ("strategic-demand", "Strategic Demand and Space Industry"),
]

QUESTION_CLUSTER_ORDER = [
    ("foundational", "Foundational Questions"),
    ("technology", "Technology"),
    ("feasibility-constraints", "Feasibility and Constraints"),
    ("safety-regulation", "Safety and Regulation"),
    ("grid-energy-systems", "Grid and Energy Systems"),
    ("ai-defense-strategic", "AI, Defense, and Strategic Demand"),
    ("program-institutional", "Programs and Institutions"),
]

TECH_CLUSTER_ORDER = [
    ("photovoltaics-power-generation", "Photovoltaics and Power Generation"),
    ("wireless-power-transmission", "Wireless Power Transmission"),
    ("receiving-conversion-systems", "Receiving and Conversion Systems"),
    ("orbital-assembly-structures", "Orbital Assembly and Structures"),
    ("launch-in-space-logistics", "Launch and In-Space Logistics"),
    ("thermal-management-systems", "Thermal Management Systems"),
    ("autonomous-operations-robotics", "Autonomous Operations and Robotics"),
]

PROGRAM_CLUSTER_ORDER = [
    ("national-space-agency", "National Space Agency Programs"),
    ("national-research-program", "National Research and Industrial Programs"),
    ("defense-military", "Defense and Military Research"),
    ("academic-university", "Academic and University Programs"),
    ("industry-consortium", "Industry and Consortium Programs"),
    ("historical-foundational", "Historical and Foundational References"),
]

SOURCE_CLASS_ORDER = [
    ("institutional-space-agency", "Institutional Space Agency Sources"),
    ("government-policy", "Government Policy and Commissioned Studies"),
    ("academic-research", "Academic and Peer-Reviewed Research"),
    ("technical-standard", "Technical Standards and Regulatory References"),
    ("industry-consortium", "Industry and Consortium Sources"),
    ("historical-primary", "Historical and Foundational References"),
    ("methodology-internal", "Site Methodology and Governance"),
]


def load_trial_manifest() -> dict | None:
    # v1B-D: check for v1b_d manifest first
    v1b_d_path = DATA_DIR / "publication_v1b_d.json"
    if v1b_d_path.exists():
        return load_json(v1b_d_path)
    v1b_c_path = DATA_DIR / "publication_v1b_c.json"
    if v1b_c_path.exists():
        return load_json(v1b_c_path)
    v1b_b_path = DATA_DIR / "publication_v1b_b.json"
    if v1b_b_path.exists():
        return load_json(v1b_b_path)
    v1b_a_path = DATA_DIR / "publication_v1b_a.json"
    if v1b_a_path.exists():
        return load_json(v1b_a_path)
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


def _render_glossary_expansion_module(page: dict, approved_paths: set) -> str:
    if page.get("path", "") != "/":
        return ""
    glossary_link = "/glossary/"
    if glossary_link not in approved_paths:
        return ""
    parts = ['<div class="glossary-expansion-module">']
    parts.append('  <div class="glossary-expansion-header">')
    parts.append('    <span class="glossary-expansion-eyebrow">v1B — Reference Layer Expansion</span>')
    parts.append('    <h2 class="glossary-expansion-title">Glossary Source Layer Expanded</h2>')
    parts.append('  </div>')
    parts.append('  <p class="glossary-expansion-desc">The SBSP Glossary has expanded from its initial publication trial into the first v1B source layer: 53 governed terms across 5 source clusters. Definitions are source-bound, claim-boundary controlled, and internally linked to the reference infrastructure.</p>')
    parts.append('  <div class="glossary-expansion-stats">')
    parts.append('    <div class="glossary-expansion-stat"><span class="glossary-expansion-stat-value">53</span><span class="glossary-expansion-stat-label">governed terms</span></div>')
    parts.append('    <div class="glossary-expansion-stat"><span class="glossary-expansion-stat-value">5</span><span class="glossary-expansion-stat-label">source clusters</span></div>')
    parts.append('    <div class="glossary-expansion-stat"><span class="glossary-expansion-stat-value">14</span><span class="glossary-expansion-stat-label">quality validators</span></div>')
    parts.append('  </div>')
    parts.append('  <div class="glossary-expansion-clusters">')
    for _, label in CLUSTER_ORDER:
        parts.append(f'    <span class="glossary-expansion-cluster-tag">{_escape_html(label)}</span>')
    parts.append('  </div>')
    parts.append(f'  <a href="{glossary_link}" class="glossary-expansion-cta">Browse the expanded glossary</a>')
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
    expansion_html = _render_glossary_expansion_module(page, approved_paths)
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
    {expansion_html}
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


def generate_program_html(program: dict, page: dict, question_paths: dict | None = None) -> str:
    """Render a program profile page. Handles both program_registry.json and program_pages.json schemas."""
    # Try richer schema fields first (program_pages.json), fall back to registry fields
    h1 = program.get("title", program.get("programName", page["title"]))
    institution = _escape_html(program.get("institution", ""))
    country = _escape_html(program.get("country_or_region", program.get("country", "")))
    start_year = program.get("startYear", "")
    status_raw = program.get("program_status", program.get("status", ""))
    status = _escape_html(status_raw.replace("_", " "))
    activity_type = _escape_html(program.get("activity_type", "").replace("_", " "))
    cluster = program.get("cluster", "")

    # Rich fields from program_pages.json
    summary = _escape_html(program.get("summary", program.get("description", "")))
    institutional_context = _escape_html(program.get("institutional_context", ""))
    sbsp_relevance = _escape_html(program.get("sbsp_relevance", ""))
    technology_relationship = _escape_html(program.get("technology_relationship", ""))
    feasibility_boundary = _escape_html(program.get("feasibility_boundary", ""))
    claim = _escape_html(program.get("claim_boundary", program.get("claimBoundary", "")))
    source_footer = _escape_html(program.get("source_footer", ""))

    # Links
    related_glossary_terms = program.get("related_glossary_terms", [])
    related_questions = program.get("related_questions", [])
    related_technology_pages = program.get("related_technology_pages", [])
    internal_links = page.get("requiredInternalLinks", [])

    meta_rows = []
    if institution:
        meta_rows.append(f'<dt>Institution</dt><dd>{institution}</dd>')
    if country:
        meta_rows.append(f'<dt>Country / Region</dt><dd>{country}</dd>')
    if start_year:
        meta_rows.append(f'<dt>Start year</dt><dd>{start_year}</dd>')
    if status:
        meta_rows.append(f'<dt>Status</dt><dd>{status}</dd>')
    if activity_type:
        meta_rows.append(f'<dt>Activity type</dt><dd>{activity_type}</dd>')
    if cluster:
        meta_rows.append(f'<dt>Programme cluster</dt><dd>{_escape_html(cluster.replace("-", " ").title())}</dd>')

    parts = ['<div class="reference-card">']
    parts.append('  <div class="reference-card-type">Program Profile</div>')
    if meta_rows:
        parts.append('  <dl class="program-meta">' + "".join(meta_rows) + '</dl>')
    parts.append('  <div class="reference-card-body">')
    if summary:
        parts.append(f'    <div class="reference-card-full"><p>{summary}</p></div>')
    parts.append('  </div>')

    if institutional_context:
        parts.append('  <div class="program-field-section">')
        parts.append('    <p class="program-field-label">Institutional Context</p>')
        parts.append(f'    <p class="program-field-body">{institutional_context}</p>')
        parts.append('  </div>')

    if sbsp_relevance:
        parts.append('  <div class="program-field-section">')
        parts.append('    <p class="program-field-label">SBSP Relevance</p>')
        parts.append(f'    <p class="program-field-body">{sbsp_relevance}</p>')
        parts.append('  </div>')

    if technology_relationship:
        parts.append('  <div class="program-field-section">')
        parts.append('    <p class="program-field-label">Technology Relationship</p>')
        parts.append(f'    <p class="program-field-body">{technology_relationship}</p>')
        parts.append('  </div>')

    if feasibility_boundary:
        parts.append('  <div class="program-field-section">')
        parts.append('    <p class="program-field-label">Feasibility Boundary</p>')
        parts.append(f'    <p class="program-field-body">{feasibility_boundary}</p>')
        parts.append('  </div>')

    if claim:
        parts.append('  <div class="reference-card-boundary">')
        parts.append('    <p class="reference-card-boundary-label">Claim Boundary</p>')
        parts.append(f'    <p class="reference-card-boundary-text">{claim}</p>')
        parts.append('  </div>')

    # Internal links from page config
    all_links = list(internal_links)

    # Add glossary term links
    if related_glossary_terms:
        for slug in related_glossary_terms[:4]:
            gpath = f"/glossary/{slug}/"
            label = slug.replace("-", " ").title()
            if gpath not in all_links:
                all_links.append(gpath)

    # Add question links (use actual page path from question_paths lookup if available)
    if related_questions:
        for qid in related_questions[:3]:
            qpath = (question_paths or {}).get(qid, f"/questions/{qid}/")
            if qpath not in all_links:
                all_links.append(qpath)

    # Add technology page links
    if related_technology_pages:
        for tpid in related_technology_pages[:2]:
            tpath = f"/technology/{tpid}/"
            if tpath not in all_links:
                all_links.append(tpath)

    if all_links:
        parts.append('  <div class="reference-card-links">')
        for lk in all_links:
            parts.append(f'    {_link_chip(lk, _path_to_label(lk))}')
        parts.append('  </div>')

    parts.append('  <div class="reference-card-source-links">')
    parts.append('    <span class="reference-card-source-label">Source &amp; methodology</span>')
    if source_footer:
        parts.append(f'    <span class="reference-card-source-label" style="font-style:italic;opacity:0.7">{source_footer}</span>')
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
    terms_by_cluster: dict[str, list] = {}
    for tid in term_ids:
        term = seed_data["glossary"].get(tid)
        if not term:
            continue
        cluster = term.get("cluster", "core-infrastructure")
        terms_by_cluster.setdefault(cluster, []).append(term)
    total_terms = sum(len(v) for v in terms_by_cluster.values())
    active_clusters = [cid for cid, _ in CLUSTER_ORDER if terms_by_cluster.get(cid)]

    parts = []
    if description:
        parts.append(f'<p class="hub-intro">{description}</p>')

    parts.append('<div class="glossary-status-panel">')
    parts.append('  <div class="glossary-status-stat"><span class="glossary-status-value">{}</span><span class="glossary-status-label">governed terms</span></div>'.format(total_terms))
    parts.append('  <div class="glossary-status-stat"><span class="glossary-status-value">{}</span><span class="glossary-status-label">source clusters</span></div>'.format(len(active_clusters)))
    parts.append('  <div class="glossary-status-stat"><span class="glossary-status-value">Yes</span><span class="glossary-status-label">source-bound definitions</span></div>')
    parts.append('  <div class="glossary-status-stat"><span class="glossary-status-value">Yes</span><span class="glossary-status-label">claim-boundary controlled</span></div>')
    parts.append('</div>')

    parts.append('<div class="glossary-expansion-note">')
    parts.append('  This glossary has expanded from the initial publication trial layer into the first v1B source layer. Terms are governed by definition, claim boundary, related terms, page links, and source and methodology discipline.')
    parts.append('</div>')

    parts.append('<nav class="glossary-cluster-jump" aria-label="Jump to cluster">')
    parts.append('  <span class="glossary-cluster-jump-label">Jump to</span>')
    for cluster_id, cluster_label in CLUSTER_ORDER:
        if not terms_by_cluster.get(cluster_id):
            continue
        anchor = f"cluster-{cluster_id}"
        parts.append(f'  <a href="#{anchor}" class="glossary-cluster-jump-link">{_escape_html(cluster_label)}</a>')
    parts.append('</nav>')

    for cluster_id, cluster_label in CLUSTER_ORDER:
        terms = terms_by_cluster.get(cluster_id, [])
        if not terms:
            continue
        anchor = f"cluster-{cluster_id}"
        parts.append(f'<div class="hub-cluster" id="{anchor}">')
        parts.append(f'  <h2 class="hub-cluster-label">{_escape_html(cluster_label)}</h2>')
        parts.append('  <ul class="glossary-index">')
        for term in terms:
            t_path = term.get("path", f"/glossary/{term.get('slug', term.get('id'))}/")
            t_name = _escape_html(term.get("term", ""))
            t_short = _escape_html(term.get("shortDefinition", ""))
            entry = f'    <li><a href="{t_path}">{t_name}</a>'
            if t_short:
                entry += f" — {t_short}"
            entry += "</li>"
            parts.append(entry)
        parts.append("  </ul>")
        parts.append("</div>")

    body = "\n".join(parts) + "\n" + _render_hub_source_footer()
    return _page_shell(page, h1, body)


def generate_questions_hub_html(page: dict, seed_data: dict, trial_manifest: dict | None) -> str:
    h1 = page.get("title", "SBSP Questions")
    description = _escape_html(page.get("description", ""))
    question_ids = (trial_manifest or {}).get("questions", [])
    questions_by_cluster: dict[str, list] = {}
    for qid in question_ids:
        q = seed_data["questions"].get(qid)
        if not q:
            continue
        cluster = q.get("cluster", "foundational")
        questions_by_cluster.setdefault(cluster, []).append(q)
    total_questions = sum(len(v) for v in questions_by_cluster.values())
    active_clusters = [cid for cid, _ in QUESTION_CLUSTER_ORDER if questions_by_cluster.get(cid)]

    parts = []
    if description:
        parts.append(f'<p class="hub-intro">{description}</p>')

    parts.append('<div class="questions-status-panel">')
    parts.append(f'  <div class="questions-status-stat"><span class="questions-status-value">{total_questions}</span><span class="questions-status-label">reference questions</span></div>')
    parts.append(f'  <div class="questions-status-stat"><span class="questions-status-value">{len(active_clusters)}</span><span class="questions-status-label">question clusters</span></div>')
    parts.append('  <div class="questions-status-stat"><span class="questions-status-value">Yes</span><span class="questions-status-label">answer boundaries</span></div>')
    parts.append('  <div class="questions-status-stat"><span class="questions-status-value">Yes</span><span class="questions-status-label">source-disciplined</span></div>')
    parts.append('</div>')

    parts.append('<div class="questions-expansion-note">')
    parts.append('  This Q&amp;A layer has expanded from the initial publication trial into the first v1B reference layer. Every answer carries an explicit boundary separating established knowledge from unproven commercial claims.')
    parts.append('</div>')

    parts.append('<nav class="questions-cluster-jump" aria-label="Jump to question cluster">')
    parts.append('  <span class="questions-cluster-jump-label">Jump to</span>')
    for cluster_id, cluster_label in QUESTION_CLUSTER_ORDER:
        if not questions_by_cluster.get(cluster_id):
            continue
        anchor = f"qcluster-{cluster_id}"
        parts.append(f'  <a href="#{anchor}" class="questions-cluster-jump-link">{_escape_html(cluster_label)}</a>')
    parts.append('</nav>')

    for cluster_id, cluster_label in QUESTION_CLUSTER_ORDER:
        qs = questions_by_cluster.get(cluster_id, [])
        if not qs:
            continue
        anchor = f"qcluster-{cluster_id}"
        parts.append(f'<div class="hub-cluster" id="{anchor}">')
        parts.append(f'  <h2 class="hub-cluster-label">{_escape_html(cluster_label)}</h2>')
        parts.append('  <ul class="questions-index">')
        for q in qs:
            q_path = q.get("path", f"/questions/{q.get('slug', q.get('id'))}/")
            q_text = _escape_html(q.get("question", ""))
            parts.append(f'    <li><a href="{q_path}">{q_text}</a></li>')
        parts.append("  </ul>")
        parts.append("</div>")

    body = "\n".join(parts) + "\n" + _render_hub_source_footer()
    return _page_shell(page, h1, body)


def generate_technology_page_html(tech_page: dict, page: dict) -> str:
    h1 = tech_page.get("title", page["title"])
    summary = _escape_html(tech_page.get("summary", ""))
    infra_role = _escape_html(tech_page.get("infrastructureRole", ""))
    subsystem = _escape_html(tech_page.get("subsystemRelationship", ""))
    feasibility = _escape_html(tech_page.get("feasibilityBoundary", ""))
    claim = _escape_html(tech_page.get("claimBoundary", ""))
    internal_links = page.get("requiredInternalLinks", [])

    parts = ['<div class="reference-card">']
    parts.append('  <div class="reference-card-type">Technology Reference</div>')
    parts.append('  <div class="reference-card-body">')
    if summary:
        parts.append(f'    <div class="reference-card-full"><p>{summary}</p></div>')
    parts.append('  </div>')
    if infra_role:
        parts.append('  <div class="reference-card-section">')
        parts.append('    <p class="reference-card-section-label">Infrastructure Role</p>')
        parts.append(f'    <p class="reference-card-section-body">{infra_role}</p>')
        parts.append('  </div>')
    if subsystem:
        parts.append('  <div class="reference-card-section">')
        parts.append('    <p class="reference-card-section-label">Subsystem Relationship</p>')
        parts.append(f'    <p class="reference-card-section-body">{subsystem}</p>')
        parts.append('  </div>')
    if feasibility:
        parts.append('  <div class="reference-card-section">')
        parts.append('    <p class="reference-card-section-label">Feasibility and Readiness</p>')
        parts.append(f'    <p class="reference-card-section-body">{feasibility}</p>')
        parts.append('  </div>')
    if claim:
        parts.append('  <div class="reference-card-boundary">')
        parts.append('    <p class="reference-card-boundary-label">Feasibility and Claim Boundary</p>')
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


def generate_technology_hub_html(page: dict, seed_data: dict, trial_manifest: dict | None) -> str:
    h1 = page.get("title", "SBSP Technology Reference")
    description = _escape_html(page.get("description", ""))
    tech_ids = (trial_manifest or {}).get("technologyPages", [])
    tech_by_cluster: dict[str, list] = {}
    for tid in tech_ids:
        tp = seed_data["technology"].get(tid)
        if not tp:
            continue
        cluster = tp.get("cluster", "photovoltaics-power-generation")
        tech_by_cluster.setdefault(cluster, []).append(tp)
    total_tech = sum(len(v) for v in tech_by_cluster.values())
    active_clusters = [cid for cid, _ in TECH_CLUSTER_ORDER if tech_by_cluster.get(cid)]

    parts = []
    if description:
        parts.append(f'<p class="hub-intro">{description}</p>')

    parts.append('<div class="tech-status-panel">')
    parts.append(f'  <div class="tech-status-stat"><span class="tech-status-value">{total_tech}</span><span class="tech-status-label">technology pages</span></div>')
    parts.append(f'  <div class="tech-status-stat"><span class="tech-status-value">{len(active_clusters)}</span><span class="tech-status-label">engineering clusters</span></div>')
    parts.append('  <div class="tech-status-stat"><span class="tech-status-value">Yes</span><span class="tech-status-label">claim boundaries</span></div>')
    parts.append('  <div class="tech-status-stat"><span class="tech-status-value">Yes</span><span class="tech-status-label">feasibility-bounded</span></div>')
    parts.append('</div>')

    parts.append('<div class="tech-expansion-note">')
    parts.append('  This technology reference layer covers 21 governed entries across 7 engineering clusters. Each entry provides a technical definition, infrastructure role, subsystem relationship, feasibility boundary, and explicit claim boundary separating documented knowledge from unverified projections.')
    parts.append('</div>')

    parts.append('<nav class="tech-cluster-jump" aria-label="Jump to technology cluster">')
    parts.append('  <span class="tech-cluster-jump-label">Jump to</span>')
    for cluster_id, cluster_label in TECH_CLUSTER_ORDER:
        if not tech_by_cluster.get(cluster_id):
            continue
        anchor = f"tcluster-{cluster_id}"
        parts.append(f'  <a href="#{anchor}" class="tech-cluster-jump-link">{_escape_html(cluster_label)}</a>')
    parts.append('</nav>')

    for cluster_id, cluster_label in TECH_CLUSTER_ORDER:
        tps = tech_by_cluster.get(cluster_id, [])
        if not tps:
            continue
        anchor = f"tcluster-{cluster_id}"
        parts.append(f'<div class="hub-cluster" id="{anchor}">')
        parts.append(f'  <h2 class="hub-cluster-label">{_escape_html(cluster_label)}</h2>')
        parts.append('  <ul class="tech-index">')
        for tp in tps:
            tp_path = tp.get("path", f"/technology/{tp.get('slug', tp.get('id'))}/")
            tp_title = _escape_html(tp.get("title", ""))
            parts.append(f'    <li><a href="{tp_path}">{tp_title}</a></li>')
        parts.append('  </ul>')
        parts.append('</div>')

    body = "\n".join(parts) + "\n" + _render_hub_source_footer()
    return _page_shell(page, h1, body)


def generate_programs_hub_html(page: dict, seed_data: dict, trial_manifest: dict | None) -> str:
    """v1B-D: Upgraded program hub with cluster grouping, status panel, expansion note, cluster jump nav."""
    h1 = page.get("title", "SBSP Program Profiles")
    description = _escape_html(page.get("description", ""))
    program_ids = (trial_manifest or {}).get("programs", [])

    programs_by_cluster: dict[str, list] = {}
    for pid in program_ids:
        prog = seed_data["programs"].get(pid)
        if not prog:
            continue
        cluster = prog.get("cluster", "national-space-agency")
        programs_by_cluster.setdefault(cluster, []).append(prog)

    total_programs = sum(len(v) for v in programs_by_cluster.values())
    active_clusters = [cid for cid, _ in PROGRAM_CLUSTER_ORDER if programs_by_cluster.get(cid)]

    parts = []
    if description:
        parts.append(f'<p class="hub-intro">{description}</p>')

    # Status panel
    parts.append('<div class="program-status-panel">')
    parts.append(f'  <div class="program-status-stat"><span class="program-status-value">{total_programs}</span><span class="program-status-label">program profiles</span></div>')
    parts.append(f'  <div class="program-status-stat"><span class="program-status-value">{len(active_clusters)}</span><span class="program-status-label">institutional clusters</span></div>')
    parts.append('  <div class="program-status-stat"><span class="program-status-value">Yes</span><span class="program-status-label">claim boundaries</span></div>')
    parts.append('  <div class="program-status-stat"><span class="program-status-value">Yes</span><span class="program-status-label">source-disciplined</span></div>')
    parts.append('</div>')

    # Expansion note
    parts.append('<div class="program-expansion-note">')
    parts.append(f'  This institutional intelligence layer covers {total_programs} governed program profiles across {len(active_clusters)} clusters. Each entry documents agency, programme, or research activity context, SBSP relevance, technology relationship, feasibility boundary, and explicit claim boundary. Timelines from programme roadmaps are identified as planning targets, not funded commitments.')
    parts.append('</div>')

    # Cluster jump nav
    parts.append('<nav class="program-cluster-jump" aria-label="Jump to program cluster">')
    parts.append('  <span class="program-cluster-jump-label">Jump to</span>')
    for cluster_id, cluster_label in PROGRAM_CLUSTER_ORDER:
        if not programs_by_cluster.get(cluster_id):
            continue
        anchor = f"pcluster-{cluster_id}"
        parts.append(f'  <a href="#{anchor}" class="program-cluster-jump-link">{_escape_html(cluster_label)}</a>')
    parts.append('</nav>')

    # Cluster sections
    for cluster_id, cluster_label in PROGRAM_CLUSTER_ORDER:
        progs = programs_by_cluster.get(cluster_id, [])
        if not progs:
            continue
        anchor = f"pcluster-{cluster_id}"
        parts.append(f'<div class="hub-cluster" id="{anchor}">')
        parts.append(f'  <h2 class="hub-cluster-label">{_escape_html(cluster_label)}</h2>')
        parts.append('  <ul class="programs-cluster-index">')
        for prog in progs:
            p_path = prog.get("path", f"/programs/{prog.get('slug', prog.get('id'))}/")
            p_title = _escape_html(prog.get("title", prog.get("programName", "")))
            p_inst = _escape_html(prog.get("institution", ""))
            p_country = _escape_html(prog.get("country_or_region", prog.get("country", "")))
            entry = f'    <li><a href="{p_path}">{p_title}</a>'
            if p_inst:
                entry += f'<span class="prog-institution"> — {p_inst}'
                if p_country:
                    entry += f' ({p_country})'
                entry += '</span>'
            entry += '</li>'
            parts.append(entry)
        parts.append('  </ul>')
        parts.append('</div>')

    body = "\n".join(parts) + "\n" + _render_hub_source_footer()
    return _page_shell(page, h1, body)


def generate_sources_hub_html(page: dict, seed_data: dict) -> str:
    """v1B-E: Governed source registry hub with status panel, class sections, and governance explanation."""
    h1 = page.get("title", "Sources and Claim Boundaries")
    description = _escape_html(page.get("description", ""))

    records = seed_data.get("sources", [])
    by_class: dict[str, list] = {}
    for rec in records:
        sc = rec.get("source_class", "")
        by_class.setdefault(sc, []).append(rec)

    total_sources = len(records)
    active_classes = [cid for cid, _ in SOURCE_CLASS_ORDER if by_class.get(cid)]

    parts = []
    if description:
        parts.append(f'<p class="hub-intro">{description}</p>')

    # Status panel
    parts.append('<div class="source-status-panel">')
    parts.append(f'  <div class="source-status-stat"><span class="source-status-value">{total_sources}</span><span class="source-status-label">governed sources</span></div>')
    parts.append(f'  <div class="source-status-stat"><span class="source-status-value">{len(active_classes)}</span><span class="source-status-label">source classes</span></div>')
    parts.append('  <div class="source-status-stat"><span class="source-status-value">Yes</span><span class="source-status-label">claim boundaries</span></div>')
    parts.append('  <div class="source-status-stat"><span class="source-status-value">Yes</span><span class="source-status-label">verification posture</span></div>')
    parts.append('</div>')

    # Governance explanation
    parts.append('<div class="source-governance-note">')
    parts.append('  <p>This registry governs the evidence base for Space-Based-Solar-Power.com. Each source record documents authority role, claim scope, verification posture, and explicit boundary notes. Sources are classified into seven institutional categories. No source is treated as unconditional authority — all are bounded by what they can and cannot establish.</p>')
    parts.append('</div>')

    # How sources are used
    parts.append('<div class="source-usage-section">')
    parts.append('  <h2>How sources are used</h2>')
    parts.append('  <p>Sources are applied according to a three-tier hierarchy. Tier 1 sources (institutional space agencies, government policy) establish the primary reference baseline. Tier 2 sources (academic research, technical standards) provide analytical and experimental grounding. Tier 3 sources (industry and consortium) are used only for documenting institutional activity and company claims — never to establish independent technical claims. Internal methodology sources govern editorial practice, not external claims.</p>')
    parts.append('  <p>Claim boundaries on every page specify which source tier supports each category of claim, and where claims remain unresolved, contested, or dependent on assumptions. See <a href="/methodology/">Methodology</a> for the full claim classification framework.</p>')
    parts.append('</div>')

    # Claim boundary explanation
    parts.append('<div class="source-claim-boundary">')
    parts.append('  <h2>Source governance and claim boundaries</h2>')
    parts.append('  <p>Every page on this site carries an explicit claim boundary statement. That statement identifies which claims are source-verified, which are institutional summaries, which are technical explanations with modelled assumptions, which are company claims requiring independent verification, and which remain genuinely unresolved.</p>')
    parts.append('  <p>No source record in this registry is used to assert that space-based solar power is commercially deployed, operational at utility scale, or a proven full infrastructure system. The current state of SBSP is pre-deployment: technology components are at varying readiness levels, programmes are in feasibility study or early demonstration phases, and no operational system exists as of the date of this page.</p>')
    parts.append('</div>')

    # Class jump nav
    parts.append('<nav class="source-class-jump" aria-label="Jump to source class">')
    parts.append('  <span class="source-class-jump-label">Jump to</span>')
    for class_id, class_label in SOURCE_CLASS_ORDER:
        if not by_class.get(class_id):
            continue
        anchor = f"sclass-{class_id}"
        parts.append(f'  <a href="#{anchor}" class="source-class-jump-link">{_escape_html(class_label)}</a>')
    parts.append('</nav>')

    # Class sections
    for class_id, class_label in SOURCE_CLASS_ORDER:
        recs = by_class.get(class_id, [])
        if not recs:
            continue
        anchor = f"sclass-{class_id}"
        parts.append(f'<div class="source-class-section" id="{anchor}">')
        parts.append(f'  <h2 class="source-class-label">{_escape_html(class_label)}</h2>')
        parts.append('  <ul class="source-class-index">')
        for rec in recs:
            label = _escape_html(rec.get("label", ""))
            authority = _escape_html(rec.get("authority_role", ""))
            parts.append(f'    <li class="source-record">')
            parts.append(f'      <span class="source-label">{label}</span>')
            if authority:
                parts.append(f'      <span class="source-authority"> — {authority}</span>')
            cs = _escape_html(rec.get("claim_scope", ""))
            if cs:
                parts.append(f'      <p class="source-claim-scope">{cs}</p>')
            bn = _escape_html(rec.get("boundary_notes", ""))
            if bn:
                parts.append(f'      <p class="source-boundary-note"><strong>Boundary:</strong> {bn}</p>')
            parts.append(f'    </li>')
        parts.append('  </ul>')
        parts.append('</div>')

    # Footer links
    footer_links = [
        ('/methodology/', 'Methodology'),
        ('/framework/', 'Framework'),
        ('/feasibility-and-constraints/', 'Feasibility and Constraints'),
        ('/strategic-importance/', 'Strategic Importance'),
        ('/global-programs/', 'Global Programs'),
        ('/programs/', 'Program Profiles'),
        ('/glossary/', 'Glossary'),
        ('/questions/', 'Questions'),
        ('/technology/', 'Technology'),
    ]
    parts.append('<div class="hub-source-links">')
    parts.append('<span class="hub-source-label">Related reference layers</span>')
    for path, label in footer_links:
        parts.append(f'<a class="link-chip" href="{path}">{_escape_html(label)}</a>')
    parts.append('</div>')

    body = "\n".join(parts)
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
        html = generate_program_html(program, page, seed_data.get("question_paths")) if program else generate_html(page, content, approved_paths)
    elif seed_data and seed_source == "glossary_hub":
        html = generate_glossary_hub_html(page, seed_data, trial_manifest)
    elif seed_data and seed_source == "questions_hub":
        html = generate_questions_hub_html(page, seed_data, trial_manifest)
    elif seed_data and seed_source == "programs_hub":
        html = generate_programs_hub_html(page, seed_data, trial_manifest)
    elif seed_data and seed_source == "technology":
        tech_page = seed_data["technology"].get(seed_id)
        html = generate_technology_page_html(tech_page, page) if tech_page else generate_html(page, content, approved_paths)
    elif seed_data and seed_source == "technology_hub":
        html = generate_technology_hub_html(page, seed_data, trial_manifest)
    elif seed_data and seed_source == "sources_hub":
        html = generate_sources_hub_html(page, seed_data)
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
        "technology": [],
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
        elif path.startswith("/technology/") and path != "/technology/":
            categories["technology"].append(p)
        else:
            categories["core"].append(p)
    return categories


def build_sitemaps(all_sitemap_urls: list, categories: dict) -> list:
    sitemap_files = []

    core_urls = generate_sitemap_urls(categories["core"])
    if core_urls:
        sf = SITEMAPS_DIR / "sitemap-core.xml"
        write_sitemap_file(core_urls, sf)
        sitemap_files.append("sitemaps/sitemap-core.xml")

    for cat_name in ["glossary", "questions", "programs", "countries",
                     "articles", "usecases", "comparisons", "sources", "technology"]:
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
