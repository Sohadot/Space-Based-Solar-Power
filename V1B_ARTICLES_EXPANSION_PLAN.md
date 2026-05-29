# V1B-F Articles & Strategic Briefs Expansion — Implementation Plan

## Sprint: v1B-F
## Branch: claude/v1b-f-articles-expansion-cm4aq
## Prerequisite: v1B-E merged, deployed, live verified (V1B-DL-011 on main)

---

## Scope

Add 12 governed strategic brief pages under `/articles/` across 4 thematic clusters. Each article is a data-governed editorial page with substantive content, explicit feasibility and claim boundaries, and cross-references to glossary, questions, technology, and program pages.

---

## Clusters and Articles

### infrastructure-strategy (3 articles)
- `sbsp-as-strategic-infrastructure` — Why SBSP is categorised as infrastructure, not product
- `orbital-energy-node-grid-architecture` — Grid integration: rectenna fields, power delivery, grid role
- `sbsp-development-pathway` — The pathway from demonstration to infrastructure-scale deployment

### technology-feasibility (3 articles)
- `wireless-power-transmission-scale` — WPT technical thresholds and current demonstration state
- `launch-economics-viability` — Launch cost threshold problem and SBSP economic sensitivity
- `technology-readiness-feasibility-frontier` — TRL analysis across SBSP subsystems

### institutional-programs (3 articles)
- `esa-solaris-european-rationale` — ESA SOLARIS: assessment process, conclusions, and what was not resolved
- `caltech-maple-what-demonstration-means` — What MAPLE established and what it did not demonstrate
- `national-sbsp-programmes-comparison` — Comparing NASA, ESA, JAXA, and national programme approaches

### energy-sovereignty-ai (3 articles)
- `ai-infrastructure-energy-demand` — AI power demand characteristics and structural SBSP relevance
- `energy-sovereignty-strategic-rationale` — Energy sovereignty framing and strategic investment evaluation
- `sbsp-defense-energy-logistics` — Defence energy logistics case and US institutional investment

---

## Files Created or Modified

### New Files
- `main/data/article_pages.json` — 12 governed article records
- `main/data/publication_v1b_f.json` — Trial manifest inheriting v1b_d content, adding articles list
- `main/scripts/validate_articles.py` — 16th quality gate validator

### Modified Files
- `main/scripts/quality_gate.py` — VALIDATORS list extended from 15 to 16 entries
- `main/scripts/build.py` — Article loading, program_paths lookup, article hub/page generators, routing
- `main/data/pages.json` — Articles hub entry + 12 article_brief entries (189 total approved pages)
- `main/data/internal_link_graph.json` — `article_brief` rule added; articles hub maxOutboundLinks updated
- `main/static/css/main.css` — Article hub and individual article page styles

---

## Validation Schema (validate_articles.py)

Each article record must pass:
- Unique `id` and `slug`
- All 14 required fields present and non-empty
- `cluster` is one of 4 allowed values
- `summary` ≥ 150 characters
- `seoTitle` ≤ 70 characters
- `seoDescription` ≤ 160 characters
- No banned phrases (commercially deployed, operational at utility scale, etc.)
- `relatedGlossaryTerms` ≥ 3 entries, all resolving to known glossary slugs
- `relatedQuestions` ≥ 3 entries, all resolving to known question IDs
- `relatedTechnologyPages` entries (if present) resolving to known technology page IDs
- `relatedPrograms` entries (if present) resolving to known program IDs
- All 4 clusters represented across the article set

---

## Technical Notes

### program_paths Lookup
`load_seed_data()` builds a `program_paths` dict in two passes:
1. From `pages.json` program_profile entries (seedId → path)
2. From `program_pages.json` entries (id → path field)

This resolves cases where a program's data ID (e.g. `nasa-sbsp-revisit`) differs from its pages.json seedId (e.g. `nasa-space-solar-power-revisit`) — both map to the correct public path.

### publication_v1b_f.json
Extends publication_v1b_d.json content: inherits all glossaryTerms, questions, programs, technologyPages lists plus adds the articles list. Hub generators for glossary, questions, and programs read from this manifest; it must include all content keys to prevent empty hubs.

### Article Hub Generator
`generate_articles_hub_html()`: status panel, cluster jump navigation, cluster-grouped article entries with summary excerpts, governance note, links to all 12 article pages.

### Article Page Generator
`generate_article_page_html()`: cluster badge, summary, strategic thesis, institutional context, technical context, feasibility boundary box, claim boundary box, related link chips (glossary, questions, technology, programs), source footer.

---

## Quality Gate Result
- Validators: 16/16 PASS
- Generated pages: 189
- Sitemap URLs: 189
- Legacy ref-nav patterns: 0

---

## Blocked Actions (Unchanged)
- No GSC submission
- No WebGL
- No JavaScript-dependent UI
- No manual public/ patching
- v1B-G BLOCKED until v1B-F merged, deployed, live verified, and V1B-DL-013 recorded
