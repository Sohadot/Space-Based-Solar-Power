# Reference Launch v1B — Controlled Expansion Plan

## Purpose

This plan governs the controlled 300–500 page expansion of Space-Based-Solar-Power.com after Sprint 2 (interface correction) is merged and quality-gate approved.

The v1B launch is not a small symbolic batch. It is a serious reference launch organized into defined content clusters, each with a target count, page type, data source, boundary requirement, internal link plan, sitemap eligibility rule, validation requirement, and publication trigger.

No cluster may be published unless it is complete, internally linked, source-disciplined, quality-gate approved, and consistent with the Sovereign Spatial Interface template system established in Sprint 2.

---

## Prerequisites Before Any v1B Work Begins

1. Sprint 2 (`claude/strategic-direction-v1b-tYbVs`) merged to `main` and quality gate green.
2. Sovereign Spatial Interface templates active in `build.py` and `main/static/css/main.css`.
3. No Google Search Console submission until Sprint 2 is reviewed.
4. No bulk content generation until cluster data files are prepared and reviewed.

---

## Cluster Architecture

The v1B launch is organized across eight content clusters. Target total: 210–310 new pages, bringing the overall publication count to approximately 300–500 pages when combined with the existing 39-page foundation.

---

## Cluster 1 — Technology Pages

| Field | Value |
|---|---|
| Target count | 30–50 pages |
| Page type | `technology_reference` |
| Data source file | `main/data/technology_terms.json` (new) |
| Required boundaries | `claimBoundary` required on every page |
| Internal link requirements | Each page links to `/technology-stack/`; related glossary terms; at least one program page where relevant |
| Sitemap eligibility | Yes, all approved technology pages |
| Validation rules | Schema, content, links, sources, claims, SEO, sitemap, internal-link graph |
| Publication trigger | Cluster complete (minimum 30 pages passing full quality gate) |

### Examples

- Solar power satellite architecture
- Orbital solar array design
- Microwave power beaming fundamentals
- Laser power transmission overview
- Rectenna design and efficiency
- In-space assembly concepts
- Orbital station-keeping requirements
- Space debris and SBSP orbital environment
- Launch vehicle requirements for SBSP payloads
- Power management and distribution from orbit

### Boundary requirement

All technology pages must include a `claimBoundary` field stating the source basis and technology readiness level context. No page may assert commercial maturity, economic viability, or deployment readiness without a documented source boundary.

---

## Cluster 2 — Constraint Pages

| Field | Value |
|---|---|
| Target count | 20–30 pages |
| Page type | `constraint_analysis` |
| Data source file | `main/data/constraint_registry.json` (new) |
| Required boundaries | `claimBoundary` required on every page |
| Internal link requirements | Each page links to `/feasibility-and-constraints/`; related technology pages; at least one source brief |
| Sitemap eligibility | Yes, all approved constraint pages |
| Validation rules | Schema, content, links, sources, claims, SEO, sitemap, internal-link graph |
| Publication trigger | Cluster complete (minimum 20 pages passing full quality gate) |

### Constraint taxonomy (primary categories)

- Launch economics and cost reduction requirements
- Orbital assembly complexity and automation
- Microwave transmission efficiency and atmospheric loss
- Laser transmission atmospheric interference
- Beam safety and regulatory certification
- Rectenna land area and siting constraints
- Grid integration and load management
- In-orbit operations and maintenance
- Space debris risk and mitigation
- Capital formation and financing barriers
- Public legitimacy and social acceptance
- International coordination and spectrum allocation
- Long-term orbital lifecycle and decommissioning

### Boundary requirement

All constraint pages must state whether the constraint is: currently active, partially mitigated, resolved under specific scenarios, or dependent on future technological development. No page may describe a constraint as definitively resolved without a Tier 1 or Tier 2 source.

---

## Cluster 3 — Glossary Pages

| Field | Value |
|---|---|
| Target count | 60–80 pages |
| Page type | `glossary_term` |
| Data source file | `main/data/glossary_terms.json` (existing — expand) |
| Required boundaries | `claimBoundary` required on every term |
| Internal link requirements | Each term links to `/glossary/` hub; at least 2 related terms; at least 1 foundation page |
| Sitemap eligibility | Yes, all approved glossary terms |
| Validation rules | Schema, content, links, sources, claims, SEO, sitemap, internal-link graph |
| Publication trigger | Cluster complete (minimum 50 terms passing full quality gate) |

### Coverage targets

- SBSP system terms: solar power satellite, rectenna, power beaming, microwave transmission, laser transmission, in-space assembly, orbital array, wireless power transmission
- Policy and strategy terms: energy sovereignty, grid resilience, remote power, defense logistics, critical infrastructure, space industrial base
- Technical readiness terms: technology readiness level, system readiness level, demonstration, proof of concept, commercial feasibility
- Program terms: SOLARIS, SSPS, SSPD, SPS-ALPHA, CASSIOPeiA, Arachne
- Infrastructure terms: geosynchronous orbit, low Earth orbit, medium Earth orbit, orbital mechanics, attitude control, power management and distribution
- Cross-domain terms: AI energy demand, data center power density, hyperscale computing, orbital manufacturing, lunar power infrastructure

### Boundary requirement

Every glossary term must include a `claimBoundary` stating the scope and limits of the definition. Terms with contested definitions must note the definitional boundary explicitly.

---

## Cluster 4 — Question Pages

| Field | Value |
|---|---|
| Target count | 50–70 pages |
| Page type | `question` |
| Data source file | `main/data/question_bank.json` (existing — expand) |
| Required boundaries | `answerBoundary` required on every question |
| Internal link requirements | Each question links to `/questions/` hub; at least 2 related pages |
| Sitemap eligibility | Yes, all approved question pages |
| Validation rules | Schema, content, links, sources, claims, SEO, sitemap, internal-link graph |
| Publication trigger | Cluster complete (minimum 40 questions passing full quality gate) |

### Question categories

- Definition questions: What is SBSP? What is a solar power satellite? What is wireless power transmission?
- Feasibility questions: How far is SBSP from commercial deployment? What are the main barriers? How do launch costs affect SBSP?
- Comparison questions: How does SBSP compare to terrestrial solar? Why is SBSP different from satellite-based observation?
- Strategic questions: Why does energy sovereignty matter for SBSP? How does SBSP relate to AI energy demand? Why is SBSP relevant for defense?
- Program questions: What is ESA Solaris? What is JAXA SSPS? What did the Caltech SSPD demonstrate?
- Investor questions: What should investors know about SBSP? What is the commercial maturity status?
- Journalist questions: What claims about SBSP are supported? What is not yet proven?

### Boundary requirement

Every question answer must include an `answerBoundary` stating the evidence basis and what remains uncertain. No answer may claim SBSP is commercially ready, economically inevitable, or technically resolved without a source boundary.

---

## Cluster 5 — Program Profiles

| Field | Value |
|---|---|
| Target count | 20–30 pages |
| Page type | `program_profile` |
| Data source file | `main/data/program_registry.json` (existing — expand) |
| Required boundaries | `claimBoundary` required on every profile |
| Internal link requirements | Each profile links to `/programs/` hub; `/global-programs/`; related technology pages; relevant sources |
| Sitemap eligibility | Yes, all approved program profiles |
| Validation rules | Schema, content, links, sources, claims, SEO, sitemap, internal-link graph |
| Publication trigger | Cluster complete (minimum 15 profiles passing full quality gate) |

### Program coverage targets

- Institutional programs: ESA Solaris, JAXA SSPS, NASA OTPS study, UK Space Energy Initiative, China SBSP research
- Academic programs: Caltech SSPD, MIT research, ETH Zurich work
- Enterprise programs: Airbus SOLARIS participation, Astroscale SBSP concept, Northrop Grumman space solar involvement
- Historical programs: NASA SPS concept study (1979), DOE/NASA reference system

### Boundary requirement

All program profiles must distinguish between: institutional research programs, demonstration projects, commercial development programs, and government-funded studies. Enterprise disclosures must be treated as company claims unless independently supported. No profile may describe a program as beyond its documented status.

---

## Cluster 6 — Audience Guides

| Field | Value |
|---|---|
| Target count | 10–15 pages |
| Page type | `audience_guide` |
| Data source file | `main/data/audience_guides.json` (new) |
| Required boundaries | Recommended but not required |
| Internal link requirements | Each guide links to `/framework/`; relevant tools; at least 3 reference pages relevant to audience |
| Sitemap eligibility | Yes, all approved audience guides |
| Validation rules | Schema, content, links, SEO, sitemap, internal-link graph |
| Publication trigger | Cluster complete (minimum 6 guides passing full quality gate) |

### Audience guide targets

- SBSP for researchers: what to study, where to start, key sources
- SBSP for journalists: how to report responsibly, key claim boundaries, what is unresolved
- SBSP for investors: what to assess, readiness indicators, due diligence questions
- SBSP for governments: strategic framing, energy sovereignty context, program landscape
- SBSP for engineers: technical entry points, constraint landscape, program connections
- SBSP for AI and data center companies: energy demand context, future supply options
- SBSP for defense and resilience planners: strategic power continuity logic
- SBSP for general serious readers: foundational understanding without hype

---

## Cluster 7 — Source Briefs

| Field | Value |
|---|---|
| Target count | 15–25 pages |
| Page type | `source_brief` |
| Data source file | `main/data/sources.json` (existing — extend with brief fields) |
| Required boundaries | `claimBoundary` required (what the source proves and what it does not) |
| Internal link requirements | Each brief links to `/sources/`; `/methodology/`; at least 3 pages that cite the source |
| Sitemap eligibility | Yes, all approved source briefs |
| Validation rules | Schema, content, links, SEO, sitemap, internal-link graph |
| Publication trigger | Cluster complete (minimum 10 briefs passing full quality gate) |

### Source brief targets

- NASA OTPS SBSP 2024 study brief
- ESA Solaris documentation brief
- JAXA SSPS research brief
- Caltech SSPD 2023 demonstration brief
- UK Space Energy Initiative report brief
- Historical NASA SPS 1979 reference system brief
- IAA SBSP assessment brief
- Academic peer-reviewed collection brief (by cluster)

### Boundary requirement

Every source brief must clearly state: what the source establishes, what the source does not establish, the institutional authority of the source, and when the source was published. Source briefs must not be used to extend a source's claims beyond what the source actually states.

---

## Cluster 8 — Tools / Matrix Pages

| Field | Value |
|---|---|
| Target count | 5–10 pages |
| Page type | `tool` |
| Data source file | `main/data/tools.json` (existing) |
| Required boundaries | Boundary statement required on all claim-bearing outputs |
| Internal link requirements | Each tool links to `/tools/`; `/methodology/`; relevant sources |
| Sitemap eligibility | Yes, all approved tool pages |
| Validation rules | Schema, content, links, SEO, sitemap, internal-link graph; additional tool-specific validation |
| Publication trigger | Individual tool complete and quality-gate approved (tools are published one at a time, not as a batch) |

### Tool targets for v1B

- Orbital Energy Constraint Matrix (full page, structured static table)
- SBSP Glossary Navigator (structured glossary index with search-like filtering via HTML/CSS)
- Global Program Tracker (structured registry of programs with status and source links)
- Use-Case Fit Evaluator (structured guide to SBSP use-case fit by scenario)
- Claim Boundary Checker (structured reference for evaluating SBSP claims)

### Tool rules

No tool may provide financial advice, legal advice, investment recommendations, procurement recommendations, or government policy instructions. No tool may produce single-number certainty claims without methodology disclosure. Numerical models require separate documented approval.

---

## Total Cluster Summary

| Cluster | Target Pages | Page Type |
|---|---|---|
| Technology Pages | 30–50 | technology_reference |
| Constraint Pages | 20–30 | constraint_analysis |
| Glossary Pages | 60–80 | glossary_term |
| Question Pages | 50–70 | question |
| Program Profiles | 20–30 | program_profile |
| Audience Guides | 10–15 | audience_guide |
| Source Briefs | 15–25 | source_brief |
| Tools / Matrix Pages | 5–10 | tool |
| **New pages total** | **210–310** | |
| Existing pages (Sprint 1+2) | ~40 | mixed |
| **Projected total** | **~250–350** | |

With hub pages, supporting index pages, and possible audience landing pages, the full publication will reach the 300–500 page target.

---

## Cluster Sequencing

Clusters must not be published simultaneously. Publication sequencing is:

1. **Glossary cluster** — publish first (foundational terminology supports all other clusters).
2. **Question cluster** — publish second (drives direct search intent).
3. **Technology cluster** — publish third (builds technical authority layer).
4. **Constraint cluster** — publish fourth (reinforces institutional credibility).
5. **Program profiles** — publish fifth (institutional evidence layer).
6. **Audience guides** — publish sixth (routes audiences to the reference system).
7. **Source briefs** — publish seventh (strengthens source attribution across the site).
8. **Tools** — published individually as each tool is complete.

Each cluster must pass the full quality gate independently before publication. No cluster may be published partially.

---

## Internal Link Architecture

Each cluster must be connected to the site graph before publication:

- All glossary terms link to `/glossary/` hub.
- All question pages link to `/questions/` hub.
- All program profiles link to `/programs/` hub and `/global-programs/`.
- All technology pages link to `/technology-stack/`.
- All constraint pages link to `/feasibility-and-constraints/`.
- All audience guides link to `/framework/`.
- All source briefs link to `/sources/` and `/methodology/`.
- All tools link to `/tools/`.
- Hub pages must link back to home (`/`) and be listed in the internal-link graph.
- No cluster page may be published as an orphan.

---

## Data File Preparation Requirements

Before any cluster begins generation, its data source file must:

1. Exist in `main/data/`.
2. Pass `validate_schema.py` with all required fields present.
3. Pass `validate_content.py` with no placeholder text, thin content, or AI filler.
4. Pass `validate_sources.py` with all sourceRef values resolved.
5. Pass `validate_claims.py` with no forbidden certainty phrases.
6. Have `claimBoundary` or `answerBoundary` defined for all entries where required.
7. Have `requiredInternalLinks` defined for all entries.
8. Have `sitemap: true` set only for entries that are ready for publication.

---

## Quality Gate Requirements Per Cluster

Each cluster publication run must pass all 8 quality gate validators:

1. `validate_schema.py` — all new pages pass schema validation.
2. `validate_content.py` — no placeholder text or thin content.
3. `validate_links.py` — all internal links resolve to approved paths.
4. `validate_sources.py` — all sourceRef values resolve to entries in `sources.json`.
5. `validate_claims.py` — no forbidden certainty phrases.
6. `validate_seo.py` — title, description, h1, canonical present on all pages.
7. `validate_sitemap.py` — all sitemap entries are approved_for_launch pages.
8. `validate_internal_link_graph.py` — no orphan pages, hub budget not exceeded.

No cluster may be published if any validator fails.

---

## Prohibited Behaviors During v1B

- No random page creation outside defined clusters.
- No weakening of any validator to pass more pages.
- No publication of partial clusters.
- No sitemap submission until each cluster passes the full quality gate.
- No localized content in v1B (multilingual editions are a separate governed phase).
- No numerical calculators or prediction tools without documented approval.
- No new external CDN dependencies.
- No changes to existing pages that weaken their source discipline or claim boundaries.

---

## Completion Criteria for v1B

The v1B reference launch is complete when:

1. All eight clusters have published at least their minimum page counts.
2. All published pages pass the full quality gate.
3. All hub pages are updated to list new cluster pages.
4. The internal-link graph connects all new pages to the site structure.
5. The sitemap is regenerated and validated.
6. The full quality gate passes on the complete publication set.
7. A new DECISION_LOG entry records v1B completion and documents the total page count, cluster breakdown, and any deviations from this plan.
