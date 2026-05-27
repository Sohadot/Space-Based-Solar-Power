# Quality Gate

## Purpose

This document defines the quality gate system for Space-Based-Solar-Power.com.

The quality gate is the final checkpoint before any content enters the public build. It is not a suggestion. It is a hard blocker.

No deployment may proceed if the quality gate fails.

The quality gate is implemented in:

```
main/scripts/quality_gate.py
```

And enforced automatically in:

```
.github/workflows/quality-gate.yml
```

---

## Validator Registry

| Validator | File | Blocks |
|---|---|---|
| Schema Validator | `validate_schema.py` | Missing required fields, wrong types, invalid values |
| Content Validator | `validate_content.py` | Thin content, placeholders, AI filler, empty sections |
| Link Validator | `validate_links.py` | Broken internal links, links to non-existent routes |
| Source Validator | `validate_sources.py` | Missing source references on technical claim pages |
| Claim Validator | `validate_claims.py` | Unsourced claims on constraint and technical pages |
| SEO Validator | `validate_seo.py` | Missing title, description, H1, canonical |
| Sitemap Validator | `validate_sitemap.py` | Non-approved URLs in sitemap, draft pages in sitemap |
| hreflang Validator | `validate_hreflang.py` | hreflang to unpublished language editions |
| Asset Validator | `validate_assets.py` | Missing CSS, JS, image files referenced by pages |
| Security Validator | `validate_security.py` | Unauthorized external scripts, mixed content |
| Accessibility Validator | `validate_accessibility.py` | Missing H1, missing alt text, broken heading hierarchy |
| Duplicate Validator | `validate_duplicates.py` | Duplicate slugs, near-duplicate content |
| Link Graph Validator | `validate_internal_link_graph.py` | Orphan pages, missing parent hubs, broken graph rules |
| Quality Gate | `quality_gate.py` | Aggregates all validators; fails build on any violation |

---

## validate_schema.py — Rules

Reads all JSON data files and validates against their defined schemas.

**Blocks:**
- Any `pages.json` entry missing a required field
- Any `glossary_terms.json` entry with an empty `definition`
- Any `question_bank.json` entry with a missing `answer`
- Any `program_registry.json` entry with an undefined `status`
- Any field type mismatch (e.g. string where boolean expected)
- Any `status` value not in the approved `publicationStatuses` set
- Any `type` value not defined in `page_blueprints.json`

---

## validate_content.py — Rules

Scans page content for quality signals.

**Blocks patterns:**
```
lorem ipsum
coming soon
todo
placeholder
[insert content here]
TBD
content pending
this page is under construction
[add content]
fake article
sample text
```

**Blocks structural failures:**
- Page with total content under the blueprint minimum length
- Page with required sections empty or absent
- Page with duplicate paragraphs (copy-paste detection)
- Page with no meaningful body text (only headings)

**Does not block:**
- Short pages that meet their blueprint minimum for their page type
- Technical pages with concise definitions (glossary terms may be brief if complete)

---

## validate_links.py — Rules

Builds an index of all routes in `public/` and validates every `<a href>` in generated pages.

**Blocks:**
- Any internal link pointing to a path not present in `public/`
- Any link to a `status: blocked` or `status: future` page
- Any link to a path with a trailing-slash mismatch
- Any link with an empty `href`

**Does not block:**
- External links (validated separately by `validate_assets.py`)
- Canonical links (validated by `validate_seo.py`)

---

## validate_sources.py — Rules

Validates that all `sourceRef` values in data files point to existing entries in `source_claims.json`.

**Blocks:**
- Any `sourceRef` referencing an ID not present in `source_claims.json`
- Any technical claim page (`constraint_page`, `technical_reference`) with zero source references
- Any `source_brief` page with a missing or empty source record

---

## validate_claims.py — Rules

Validates claim boundaries on high-risk page types.

**High-risk page types:**
```
constraint_page
technical_reference
country_profile
program_profile
claim_review
source_brief
```

**Blocks:**
- Any high-risk page with no `claimBoundary` field
- Any high-risk page containing economic projections without a `sourceRef`
- Any page containing phrases that assert technical certainty without source:
  - "will achieve", "is guaranteed", "has been proven", "definitively"
- Any `comparison_page` claiming one option is superior without citing a source

---

## validate_seo.py — Rules

**Blocks:**
- Missing `<title>` tag
- `<title>` tag over 70 characters
- Missing `<meta name="description">`
- Description under 50 characters or over 160 characters
- Missing `<link rel="canonical">`
- Canonical pointing to a different domain
- Missing `<h1>` tag
- More than one `<h1>` tag
- Pages with `sitemap: true` but `robots: noindex`
- Empty slug or slug containing spaces

---

## validate_sitemap.py — Rules

**Blocks:**
- Any URL in `sitemap.xml` or `sitemap_index.xml` that is not in `public/`
- Any URL in sitemap for a page with `sitemap: false`
- Any URL in sitemap for a page with `status: draft | future | blocked`
- Any sitemap file exceeding 50,000 URLs
- Any sitemap file not referenced in `sitemap_index.xml`
- `sitemap_index.xml` referencing a sitemap file that does not exist in `public/sitemaps/`

---

## validate_hreflang.py — Rules

**Blocks:**
- Any `hreflang` tag pointing to a language edition with `status: planned` or `status: future`
- Any `hreflang` tag pointing to a path not in `public/`
- Malformed `hreflang` values (must follow BCP 47 format)
- `x-default` pointing to a page that is not the canonical English edition

---

## validate_internal_link_graph.py — Rules

**Blocks:**
- Any page in `public/` with zero inbound links from other approved pages (orphan)
- Any page missing its required parent hub link
- Any page missing its required trust link (`/methodology/` or `/sources/`)
- Any hub page exceeding its maximum outbound link budget
- Any page violating the link rules defined in `internal_link_graph.json`

---

## validate_accessibility.py — Rules

**Blocks:**
- Missing `<h1>` (also caught by SEO validator)
- Any `<img>` without an `alt` attribute
- Any `<img>` with `alt=""` on a non-decorative image
- Heading level skips (e.g. `<h2>` followed by `<h4>` without `<h3>`)
- Pages with no `lang` attribute on `<html>`

---

## validate_security.py — Rules

**Blocks:**
- Any `<script src>` loading from an undeclared external domain
- Any inline `<script>` not explicitly approved in security policy
- HTTP resources on HTTPS pages (mixed content)
- Any `<iframe>` from an undeclared external domain
- `X-Frame-Options` or `Content-Security-Policy` headers absent from generated meta tags

---

## validate_duplicates.py — Rules

**Blocks:**
- Duplicate `slug` values across all pages in `pages.json`
- Duplicate `path` values
- Two pages with identical `title` values
- Two glossary terms with identical `definition` fields
- Two question pages with identical `question` fields
- Content similarity above 80% between two pages of the same type

---

## quality_gate.py — Aggregation Logic

Runs all validators in sequence. Collects all errors. Outputs a structured diagnostic report.

**Exit codes:**
- `0` — all validators passed; build may proceed
- `1` — one or more validators failed; build is blocked

**Report format:**
```
QUALITY GATE REPORT
===================
Date: {datetime}
Branch: {branch}
Commit: {sha}

Validator Results:
  [PASS] validate_schema
  [FAIL] validate_content
     - main/content/pages/example.json: placeholder text detected in section "overview"
  [PASS] validate_links
  [FAIL] validate_internal_link_graph
     - /glossary/rectenna/ is an orphan page (0 inbound links)

Total: 2 failures
Build: BLOCKED
```

---

## GitHub Actions Integration

The quality gate runs on:

- every push to `main`
- every pull request targeting `main`
- every push to `claude/*` branches

A failed quality gate blocks merge into `main`.

The workflow is defined in:

```
.github/workflows/quality-gate.yml
```
