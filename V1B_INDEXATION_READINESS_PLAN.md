# V1B-G Pre-GSC Indexation & Discovery Readiness — Implementation Plan

## Sprint: v1B-G
## Branch: claude/v1b-g-indexation-readiness-cm4aq
## Prerequisite: v1B-F merged, deployed, live verified (V1B-DL-013 on main)

---

## Sprint Objective

Prepare the Space-Based-Solar-Power.com asset for eventual Google Search Console submission by verifying and codifying all structural indexation requirements as a governed quality gate validator. This sprint adds no new content pages — it adds structural governance.

GSC submission is NOT performed in this sprint. That action remains explicitly blocked until separately authorized.

---

## Checks Implemented (validate_indexation_readiness.py — 17th validator)

### Sitemap Integrity
1. `sitemap.xml` exists at canonical path
2. `sitemap_index.xml` exists
3. `sitemap.xml` and `sitemap_index.xml` reference the same sub-sitemap set
4. All referenced sub-sitemap files physically exist in `public/sitemaps/`
5. Total sitemap URL count equals generated HTML page count (no drift)
6. No duplicate URLs across all sitemap files
7. Every sitemap URL resolves to a generated `public/{path}/index.html`
8. Approved sitemap paths and sitemap URL paths are in exact agreement

### robots.txt
9. `robots.txt` exists in `public/`
10. `robots.txt` Sitemap directive points to the canonical sitemap URL: `https://space-based-solar-power.com/sitemap.xml`

### Canonical Tags
11. Every generated HTML page has a `<link rel="canonical">` tag
12. Every canonical URL matches the page's actual public route (`{DOMAIN}{route}`)

### Robots Meta
13. No `noindex` robots meta tag on any approved public page

### Hub Discoverability
14. All 6 major hubs physically exist with generated index.html:
    - /glossary/, /questions/, /technology/, /programs/, /sources/, /articles/
15. Every hub (except /sources/ itself) contains at least one link to `/methodology/` and one to `/sources/`
16. /sources/ hub contains at least one link to `/methodology/`

### Legacy Navigation Patterns
17. Zero occurrences across all 189 HTML files of:
    - `<nav class="ref-nav"`
    - `aria-label="Explore"`
    - `aria-label="Related pages"`
    - `ref-nav-label`

### Orphan Detection
18. Every `index.html` in `public/` corresponds to an `approved_for_launch` path in `pages.json` — no manually patched or orphaned pages

---

## Blocked Actions

- **No GSC submission** — explicitly blocked until separately authorized
- **No WebGL** — not added in this sprint or any sprint without separate authorization
- **No JavaScript-dependent UI** — not added
- **No manual `public/` patching** — all output from `build.py` only
- **No validator weakening** — all 17 checks are genuine quality gates
- **No new content pages** — this sprint is governance, not content expansion

---

## Quality Gate Result

- Validators: 17/17 PASS
- Generated pages: 189
- Sitemap URLs: 189
- Page count = sitemap count: ✓
- Orphan pages: 0
- Legacy ref-nav patterns: 0
- All 6 hubs present with methodology/sources links: ✓
- All canonicals correct: ✓
- No noindex on approved pages: ✓
- robots.txt → canonical sitemap: ✓
- No duplicate sitemap URLs: ✓

---

## Files Changed

- `main/scripts/validate_indexation_readiness.py` — new 17th quality gate validator
- `main/scripts/quality_gate.py` — VALIDATORS extended from 16 to 17
- `V1B_INDEXATION_READINESS_PLAN.md` — this document
- `DECISION_LOG` — V1B-DL-014 prepended

---

## Next Required Step

Open PR from `claude/v1b-g-indexation-readiness-cm4aq` to `main`. After merge, deployment, and live verification, record V1B-DL-015. v1B-H remains BLOCKED until that is complete.
