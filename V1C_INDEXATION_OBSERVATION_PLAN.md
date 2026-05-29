# V1C Indexation Observation Window Plan

**Status:** Active — observation window open as of 2026-05-29
**Trigger:** V1B-DL-020 confirmed GSC sitemap fetch successful, 195 pages discovered
**Next sprint:** BLOCKED pending observation window conditions below

---

## 1. GSC Signals to Monitor

### Primary signals (check weekly minimum)

| Signal | Where | What to record |
|---|---|---|
| Coverage — Valid pages | GSC → Indexing → Pages | Count of indexed pages over time |
| Coverage — Excluded pages | GSC → Indexing → Pages → Excluded | Reasons for exclusion; any unexpected drops |
| Sitemap read status | GSC → Indexing → Sitemaps | Confirm "Opération effectuée" persists; watch for re-fetch errors |
| Discovered — currently not indexed | GSC → Indexing → Pages → Excluded | Count of pages discovered but not yet indexed |
| Crawled — currently not indexed | GSC → Indexing → Pages → Excluded | Indicates crawl/index separation; note if count rises abnormally |
| Page indexing errors | GSC → Indexing → Pages → Error | Any 404, redirect, canonical mismatch, or noindex signal |

### Secondary signals (check monthly minimum)

| Signal | Where | What to record |
|---|---|---|
| Performance — Total impressions | GSC → Performance | First impressions signal (may take 4–12 weeks post-indexation) |
| Performance — Top queries | GSC → Performance | First query signals for strategic SBSP terms |
| Performance — Top pages | GSC → Performance | Which pages receive first impressions |
| Core Web Vitals | GSC → Experience | LCP, CLS, INP status (Good / Needs Improvement / Poor) |
| Mobile Usability | GSC → Experience | Any mobile usability errors |

### Threshold alerts (act if any of these occur)

- Indexed page count drops below 150 (unexpected de-indexation)
- Sitemap status reverts to fetch error for more than 7 days
- Any approved page gains a noindex signal in GSC
- Any approved page shows a canonical mismatch in GSC
- Any approved page returns 404 in GSC coverage

---

## 2. Strategic Control Sample Pages

These pages are monitored as leading indicators. They span all major content clusters and represent the diversity of the site architecture.

### Hub pages (site structure health)
- `/` — Home
- `/glossary/` — Glossary hub
- `/questions/` — Questions hub
- `/technology/` — Technology hub
- `/programs/` — Programs hub
- `/articles/` — Articles hub
- `/tools/` — Tools hub (new in v1B-H)
- `/sources/` — Sources hub
- `/methodology/` — Methodology page

### Glossary samples (informational intent)
- `/glossary/space-based-solar-power/` — primary anchor term
- `/glossary/rectenna/` — specific technical term
- `/glossary/technology-readiness-level/` — strategic term
- `/glossary/energy-sovereignty/` — strategic term

### Questions samples (FAQ / featured snippet candidates)
- `/questions/what-is-space-based-solar-power/`
- `/questions/why-is-sbsp-not-commercially-deployed/`
- `/questions/can-sbsp-power-ai-data-centers/`
- `/questions/what-is-sbsp-and-defense/`

### Program pages samples (entity pages)
- `/programs/esa-solaris/`
- `/programs/caltech-sspp/`
- `/programs/nasa-space-solar-power-revisit/`

### Article pages samples (strategic brief cluster)
- `/articles/sbsp-as-strategic-infrastructure/`
- `/articles/energy-sovereignty-strategic-rationale/`
- `/articles/ai-infrastructure-energy-demand/`

### Tool pages samples (new layer — v1B-H)
- `/tools/sbsp-readiness-matrix/`
- `/tools/claim-boundary-classifier/`
- `/tools/buyer-logic-matrix/`

### Technology pages samples
- `/technology/microwave-power-transmission/`
- `/technology/rectenna-arrays/`
- `/technology/phased-array-transmitter-systems/`

---

## 3. Conditions That Would Justify the Next Sprint (v1C)

The following conditions must be evaluated before authorizing v1C or any new expansion sprint. All conditions are owner-authorized decisions — they are not automatically triggered.

### Condition A — Indexation baseline established
- GSC Coverage shows ≥ 100 valid indexed pages across multiple content clusters
- OR 4 weeks have elapsed since V1B-DL-020 with no indexation errors requiring technical fixes

### Condition B — No active technical blockers
- Zero indexation errors in GSC (no 404, redirect loop, noindex, canonical mismatch on approved pages)
- Quality gate on main remains 18/18 PASS
- robots.txt and sitemap.xml still correct

### Condition C — Owner strategic authorization
- Owner explicitly authorizes the next sprint scope in writing
- Sprint scope is defined before any code is written
- v1C sprint type is determined based on what GSC signals reveal (e.g., coverage gaps, content cluster gaps, performance opportunities)

### Possible v1C sprint types (decision pending signals)
These are candidates only — none is authorized until Conditions A–C are met:

- **v1C-A: Coverage expansion** — add new content clusters if indexation is healthy but coverage gaps identified
- **v1C-B: Technical SEO hardening** — fix any canonical, structured data, or Core Web Vitals issues found in GSC
- **v1C-C: Question cluster expansion** — add new Q&A pages if GSC shows query impressions for unanswered queries
- **v1C-D: International or alternate language layer** — if owner determines strategic need

---

## 4. Actions That Remain Blocked During Observation Window

The following actions are explicitly blocked until observation conditions are met and the owner authorizes a new sprint:

| Action | Status |
|---|---|
| Creating new public pages | **BLOCKED** |
| Modifying existing public page content | **BLOCKED** |
| Modifying CSS or design | **BLOCKED** |
| Modifying sitemap structure or generation | **BLOCKED** |
| Submitting additional individual sitemaps to GSC | **BLOCKED** |
| Requesting bulk URL indexing in GSC | **BLOCKED** |
| Performing bulk URL inspection in GSC | **BLOCKED** |
| Claiming pages are indexed, ranked, or discovered | **BLOCKED** |
| Opening a new sprint branch | **BLOCKED** |
| Weakening validators | **BLOCKED** |
| Manual public/ output patching | **BLOCKED** |
| Adding JavaScript-dependent UI | **BLOCKED** |
| Adding WebGL | **BLOCKED** |

---

## 5. What Must Not Change During the Observation Window

The following elements are frozen during the observation window. Any modification requires explicit owner authorization and a documented decision entry in DECISION_LOG before implementation.

### Frozen production outputs
- `public/` directory — all generated HTML, CSS, sitemap files, robots.txt
- All 195 approved pages as currently deployed
- `public/sitemap.xml` — canonical sitemap index
- `public/robots.txt`
- `public/sitemaps/sitemap-*.xml` — all 7 sub-sitemaps

### Frozen governance infrastructure
- `main/scripts/quality_gate.py` — VALIDATORS list (18 validators)
- All 18 validator scripts — no relaxation, no removal
- `DECISION_LOG` — append-only; no prior entry may be edited, removed, reordered, or compressed

### Frozen data files
- `main/data/pages.json` — 195 approved_for_launch entries
- `main/data/publication_v1b_h.json` — active trial manifest
- All content data files: glossary_terms.json, question_bank.json, technology_pages.json, program_pages.json, article_pages.json, tool_pages.json

---

## 6. Observation Window Timeline Reference

| Milestone | Date | Status |
|---|---|---|
| v1B-H merged to main (PR #16) | 2026-05-29 | ✓ Complete |
| v1B-H live verification (V1B-DL-017) | 2026-05-29 | ✓ Complete |
| GSC sitemap submitted (V1B-DL-018/019) | 2026-05-29 | ✓ Complete |
| GSC fetch confirmed, 195 pages discovered (V1B-DL-020) | 2026-05-29 | ✓ Complete |
| Indexation observation window open | 2026-05-29 | Active |
| First GSC coverage check | ~2026-06-05 | Pending |
| Indexation baseline assessment | ~2026-06-26 | Pending |
| v1C authorization decision | TBD by owner | Blocked |
