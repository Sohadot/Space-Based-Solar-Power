# Sovereign Generation Engine v1

## Purpose

This document defines the architecture, components, and operating rules of the Sovereign Generation Engine for Space-Based-Solar-Power.com.

The Generation Engine is the system that produces every public page from governed data sources. It replaces manual page creation at scale. It enforces quality, structure, and SEO integrity automatically. It makes expansion to tens of thousands of pages possible without producing weak, thin, or structurally broken content.

The engine does not replace human judgment. It enforces the conditions under which human-reviewed content can be safely published at scale.

---

## Core Principle

No page may be published unless it passes through the generation and validation pipeline.

No page exists because it was written manually into a template.

Every page exists because:

- a blueprint defines its required structure;
- a data source provides its governed content;
- the build system assembles the output;
- the validation system confirms its integrity;
- the quality gate approves its publication.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  SOVEREIGN DATA LAYER                   │
│  ontology.json  │  page_blueprints.json                 │
│  internal_link_graph.json  │  source_claims.json        │
│  topic_clusters.json  │  glossary_terms.json            │
│  program_registry.json  │  question_bank.json           │
│  comparison_matrix.json  │  audience_guides.json        │
│  country_registry.json  │  use_case_registry.json       │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                     BUILD SYSTEM                        │
│                  main/scripts/build.py                  │
│                                                         │
│  1. Reads pages.json                                    │
│  2. Reads page blueprints                               │
│  3. Reads content sources                               │
│  4. Reads ontology                                      │
│  5. Reads internal_link_graph                           │
│  6. Generates public/                                   │
│  7. Generates robots.txt                               │
│  8. Generates sitemap index + sitemaps                 │
│  9. Enforces approved-only publication                  │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  VALIDATION PIPELINE                    │
│                                                         │
│  validate_schema.py         validate_content.py         │
│  validate_links.py          validate_sources.py         │
│  validate_claims.py         validate_seo.py             │
│  validate_sitemap.py        validate_hreflang.py        │
│  validate_assets.py         validate_security.py        │
│  validate_accessibility.py  validate_duplicates.py      │
│  validate_internal_link_graph.py                        │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    QUALITY GATE                         │
│                quality_gate.py                          │
│                                                         │
│  PASS → public/ is approved for deployment              │
│  FAIL → build is blocked with diagnostic report         │
└─────────────────────────────────────────────────────────┘
```

---

## Page Type Registry

Every page in the system has a declared type. Each type has its own blueprint that enforces a different required structure.

| Type | Blueprint | Scale Target |
|---|---|---|
| `sovereign_gateway` | home blueprint | 1 |
| `trust_page` | trust blueprint | ~5 |
| `methodology_page` | methodology blueprint | ~3 |
| `reference_hub` | hub blueprint | ~20 |
| `conceptual_anchor` | manifesto blueprint | ~3 |
| `source_registry_page` | source blueprint | ~5 |
| `tools_gateway` | tool-index blueprint | ~3 |
| `tool_page` | tool blueprint | ~20 |
| `analysis_gateway` | article-index blueprint | ~3 |
| `foundational_reference` | reference blueprint | ~30 |
| `technical_reference` | reference blueprint | ~100 |
| `constraint_page` | constraint blueprint | 500–2,000 |
| `glossary_index` | glossary-index blueprint | ~5 |
| `glossary_term` | glossary-term blueprint | 500–2,000 |
| `question_answer` | question blueprint | 1,000–5,000 |
| `comparison_page` | comparison blueprint | 500–2,000 |
| `program_profile` | program blueprint | 100–1,000 |
| `country_profile` | country blueprint | 300–2,000 |
| `use_case_profile` | use-case blueprint | 500–3,000 |
| `audience_guide` | audience blueprint | ~20 |
| `source_brief` | source-brief blueprint | 500–5,000 |
| `claim_review` | claim-review blueprint | 500–5,000 |

---

## Data Sources by Page Type

| Page Type | Primary Data Source |
|---|---|
| `glossary_term` | `main/data/glossary_terms.json` |
| `question_answer` | `main/data/question_bank.json` |
| `comparison_page` | `main/data/comparison_matrix.json` |
| `country_profile` | `main/data/country_registry.json` |
| `program_profile` | `main/data/program_registry.json` |
| `use_case_profile` | `main/data/use_case_registry.json` |
| `audience_guide` | `main/data/audience_guides.json` |
| `constraint_page` | `main/data/ontology.json` + `source_claims.json` |
| `source_brief` | `main/data/source_claims.json` |
| `claim_review` | `main/data/source_claims.json` |
| Core reference pages | `main/content/pages/*.json` |

---

## Sitemap Architecture

At scale, a single sitemap.xml cannot hold all pages. The engine generates a sitemap index.

```
sitemap_index.xml
  └── sitemaps/sitemap-core.xml           (foundation pages)
  └── sitemaps/sitemap-glossary-001.xml   (glossary batch 1, up to 10k)
  └── sitemaps/sitemap-glossary-002.xml   (glossary batch 2 if needed)
  └── sitemaps/sitemap-questions-001.xml  (questions)
  └── sitemaps/sitemap-programs-001.xml   (programs)
  └── sitemaps/sitemap-countries-001.xml  (countries)
  └── sitemaps/sitemap-articles-001.xml   (articles)
  └── sitemaps/sitemap-usecases-001.xml   (use cases)
  └── sitemaps/sitemap-comparisons-001.xml
  └── sitemaps/sitemap-sources-001.xml
```

Each sitemap file must not exceed 50,000 URLs or 50MB uncompressed.

Only `sitemap: true` pages with `status: approved_for_launch` or equivalent approved statuses may enter any sitemap file.

---

## Build Output Structure

```
public/
  index.html
  about/index.html
  methodology/index.html
  framework/index.html
  manifesto/index.html
  sources/index.html
  tools/index.html
  articles/index.html
  what-is-space-based-solar-power/index.html
  technology-stack/index.html
  feasibility-and-constraints/index.html
  strategic-importance/index.html
  global-programs/index.html
  glossary/index.html
  glossary/{term}/index.html       (generated from glossary_terms.json)
  questions/{slug}/index.html      (generated from question_bank.json)
  programs/{slug}/index.html       (generated from program_registry.json)
  countries/{slug}/index.html      (generated from country_registry.json)
  use-cases/{slug}/index.html      (generated from use_case_registry.json)
  comparisons/{slug}/index.html    (generated from comparison_matrix.json)
  static/css/main.css
  static/js/
  robots.txt
  sitemap_index.xml
  sitemaps/sitemap-core.xml
  sitemaps/sitemap-glossary-001.xml
  ...
```

---

## Governance Rules

### Rule 1: No Manual Output

No file in `public/` may be written by hand. Every file is the output of `build.py`.

### Rule 2: No Unapproved Routes

The build script reads `pages.json`. Only pages with approved statuses generate public files. `blocked`, `future`, and `draft` statuses produce no output.

### Rule 3: No Sitemap Without Quality Gate

A URL enters the sitemap only after passing all validators.

### Rule 4: No Internal Link to Non-Existent Page

`validate_links.py` prevents any link to a route not present in the generated `public/`.

### Rule 5: No Orphan Pages

`validate_internal_link_graph.py` ensures every page has at least one parent, two related links, one trust link, and one next-step link.

### Rule 6: No AI Filler

`validate_content.py` blocks pages containing placeholder patterns, thin sections, lorem ipsum, and content that does not meet the minimum structure for its blueprint type.

### Rule 7: No Unreviewed Translations

`validate_hreflang.py` blocks hreflang tags for any language edition not marked `status: approved` in `pages.json`.

---

## Implementation Sequence

| Step | File | Status |
|---|---|---|
| 1 | `GENERATION_ENGINE.md` | This file |
| 2 | `DATA_MODEL.md` | Required |
| 3 | `INTERNAL_LINK_GRAPH_POLICY.md` | Required |
| 4 | `QUALITY_GATE.md` | Required |
| 5 | `SITEMAP_POLICY.md` | Required |
| 6 | `main/data/page_blueprints.json` | Required |
| 7 | `main/data/ontology.json` | Required |
| 8 | `main/data/internal_link_graph.json` | Required |
| 9 | `main/scripts/build.py` | Required |
| 10 | `main/scripts/validate_schema.py` | Required |
| 11 | `main/scripts/validate_content.py` | Required |
| 12 | `main/scripts/validate_links.py` | Required |
| 13 | `main/scripts/validate_sources.py` | Required |
| 14 | `main/scripts/validate_claims.py` | Required |
| 15 | `main/scripts/validate_seo.py` | Required |
| 16 | `main/scripts/validate_sitemap.py` | Required |
| 17 | `main/scripts/validate_internal_link_graph.py` | Required |
| 18 | `main/scripts/quality_gate.py` | Required |
| 19 | `.github/workflows/quality-gate.yml` | Required |
