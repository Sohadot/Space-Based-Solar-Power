# Sprint v1B-H — Strategic Tools & Buyer Logic Layer

**Branch:** `claude/v1b-h-tools-expansion-cm4aq`
**Date:** 2026-05-29
**Status:** COMPLETE — 18/18 PASS, 195 pages

---

## Objective

Upgrade /tools/ from a stub page into a governed static strategic tools layer with 6 reference-grade tool pages. All content is static HTML rendered from structured JSON data. No JavaScript, no fake interactivity, no placeholder content.

---

## Prior State

- v1B-G merged and verified on main (commit `e94e16b`)
- Quality gate: 17/17 PASS
- Pages: 189 generated, 189 sitemap URLs
- /tools/ was a single static stub page with no child pages

---

## Deliverables

### Data Files

**`main/data/tool_pages.json`**
Six governed tool records, each with full required schema:
- `sbsp-readiness-matrix` — Readiness Matrix: TRL-anchored subsystem readiness classification
- `claim-boundary-classifier` — Classification Reference: distinguishes demonstrated from speculative claims
- `program-comparison-atlas` — Comparison Reference: cross-programme structural comparison grid
- `technology-dependency-map` — Dependency Reference: maps technology prerequisite relationships
- `buyer-logic-matrix` — Strategic Positioning: maps value propositions to institutional buyer types
- `evidence-governance-dossier` — Evidence Reference: structured inventory of publicly verifiable evidence

**`main/data/publication_v1b_h.json`**
New trial manifest inheriting from v1b_f. totalPages=195. Adds `tools` array with 6 IDs.

**`main/data/pages.json`** (updated)
- /tools/ hub upgraded: type=`tools_hub`, seedSource=`tools_hub`
- 6 new tool_page entries: type=`tool_page`, seedSource=`tool`, status=`approved_for_launch`, phase=`publication_v1b_h`
- Total: 211 entries, 195 approved_for_launch

### Build Engine

**`main/scripts/build.py`** (updated)
- `TOOL_TYPE_LABELS` constant mapping toolType slugs to display labels
- `load_trial_manifest()` checks publication_v1b_h.json first
- `load_seed_data()` loads tools from tool_pages.json into `seed["tools"]`
- `categorize_pages()` adds "tools" category for /tools/* paths
- `build_sitemaps()` includes "tools" in the category loop
- `generate_tools_hub_html()` — renders hub with status panel (4 stats), governance note, tool entry grid with type badges, and footer links
- `generate_tool_page_html()` — renders tool type badge, strategic purpose, user audience + decision value meta, evaluationDimensions as HTML table, output interpretation, methodology/claim/source boundary boxes, related links section, source footer, hub footer links
- Routing in `write_page()` for `seeds_source=="tools_hub"` and `seed_source=="tool"`

### Validator

**`main/scripts/validate_tools.py`** (new — 18th validator)
Checks:
- Unique IDs and slugs
- All 17 required fields present and non-empty
- toolType in allowed set (6 types)
- strategicPurpose ≥ 150 chars
- decisionValue ≥ 80 chars
- seoTitle ≤ 70 chars
- seoDescription ≤ 160 chars
- 22 banned phrases absent from all text fields
- ≥ 3 relatedGlossaryTerms
- ≥ 2 relatedQuestions
- ≥ 1 relatedTechnologyPages
- evaluationDimensions is non-empty list of non-empty dicts
- Cross-reference validation for all related* arrays against their respective data files
- path starts with /tools/

**`main/scripts/quality_gate.py`** (updated)
VALIDATORS extended from 17 to 18 entries (validate_tools.py appended).

### CSS

**`main/static/css/main.css`** (updated)
New tool component styles added before reduced-motion block:
`.tool-status-panel`, `.tool-status-stat`, `.tool-status-value`, `.tool-status-label`, `.tool-governance-note`, `.tool-type-badge`, `.tool-hub-grid`, `.tool-entry`, `.tool-entry:hover`, `.tool-entry-link`, `.tool-entry-title`, `.tool-entry-purpose`, `.tool-entry-value`, `.tool-section`, `.tool-section--meta`, `.tool-matrix-wrapper`, `.tool-matrix-table`, `.tool-boundary-box`, `.tool-methodology`, `.tool-claim`, `.tool-related-section`, `.tool-link-chips`, `.tool-source-footer`, `.tool-source-label`

---

## Quality Gate Results

| Validator | Result |
|---|---|
| validate_schema.py | PASS |
| validate_content.py | PASS |
| validate_links.py | PASS |
| validate_sources.py | PASS |
| validate_claims.py | PASS |
| validate_seo.py | PASS |
| validate_sitemap.py | PASS |
| validate_internal_link_graph.py | PASS |
| validate_output_integrity.py | PASS |
| validate_decision_log.py | PASS |
| validate_glossary.py | PASS |
| validate_questions.py | PASS |
| validate_technology.py | PASS |
| validate_programs.py | PASS |
| validate_sources_registry.py | PASS |
| validate_articles.py | PASS |
| validate_indexation_readiness.py | PASS |
| validate_tools.py | PASS |
| **Total** | **18/18 PASS** |

**Generated: 195 pages | Sitemap URLs: 195 | Build: APPROVED**

---

## Issues Fixed During Sprint

1. `pages.json` description for /tools/ hub was 178 chars (limit: 160) — shortened to 154 chars
2. `pages.json` description for /tools/buyer-logic-matrix/ was 188 chars — shortened to 158 chars

---

## Governance Constraints (All Enforced)

- No JavaScript-dependent UI
- No WebGL
- No fake interactivity
- No "coming soon"
- No placeholder tools
- No generic calculators
- No manual public/ patching
- No validator weakening
- No deletion or rewriting of prior DECISION_LOG entries
- PR blocked until all local validation passes
- v1B-I remains BLOCKED until v1B-H is merged, deployed, live verified, and V1B-DL-017 is recorded
- Google Search Console submission remains BLOCKED
