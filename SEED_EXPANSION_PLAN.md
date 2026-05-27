# Sovereign Expansion Seed Pack v1A

## Purpose

This document defines the first controlled expansion pack for Space-Based-Solar-Power.com.

The Seed Pack is not a content dump. It is a controlled engine test.

After establishing the Sovereign Generation Engine v1, the first expansion must prove that the engine works end-to-end before scaling into hundreds or thousands of pages. A small but structurally complete pack validates the generation pipeline, data schemas, internal link graph, sitemap generation, quality gate, and claim discipline.

If a flaw exists in any validator or build step, a seed pack of 84 pages will expose it without creating thousands of broken or orphan pages.

---

## Pack Contents

| Data File | Content | Pages Generated | Status |
|---|---|---|---|
| `main/data/glossary_terms.json` | 30 SBSP terminology entries | 30 glossary pages | In progress |
| `main/data/question_bank.json` | 25 long-tail question entries | 25 question pages | In progress |
| `main/data/program_registry.json` | 10 institutional program entries | 10 program pages | In progress |
| `main/data/comparison_matrix.json` | 10 comparison entries | 10 comparison pages | Planned |
| `main/data/audience_guides.json` | 8 audience guide entries | 8 audience pages | Planned |
| `main/data/use_case_registry.json` | 1 qualitative tool page seed | 1 tool page | Planned |

**Total target: ~84 pages**

---

## Engine Readiness Checklist

Before merging to `main`, all items below must pass:

- [ ] `validate_schema.py` passes on all 3 seed data files
- [ ] `validate_content.py` passes — no placeholder text in any entry
- [ ] `validate_links.py` passes — all `pageLinks` resolve to existing or approved paths
- [ ] `validate_sources.py` passes — all `sourceRef` values either null or resolve
- [ ] `validate_claims.py` passes — no certainty language without claim boundary
- [ ] `validate_seo.py` passes — all entries have valid title and description
- [ ] `build.py` runs without error and generates `public/`
- [ ] `validate_sitemap.py` passes — sitemap contains only approved entries
- [ ] `validate_internal_link_graph.py` passes — no orphan pages
- [ ] `quality_gate.py` exits 0 (APPROVED)
- [ ] GitHub Actions workflow completes green on push

---

## Expansion Phase Map

### v1A — Seed Pack (current)

```
~84 pages
30 glossary terms
25 questions
10 programs
10 comparisons
8 audience guides
1 tool page
```

Purpose: verify engine integrity.

### v1B — First Expansion Wave

```
300–500 pages
150 glossary terms
100 questions
50 program profiles
50 constraint pages
50 comparisons
25 use-case profiles
25 source briefs
```

Purpose: establish deep topical authority in SBSP core clusters.

### v1C — Second Expansion Wave

```
1,000–2,000 pages
500 glossary terms
400 questions
150 program profiles
200 constraint pages
150 comparisons
100 country/regional entries
100 use-case profiles
100 source briefs
```

Purpose: enter the range where topical authority becomes signal-grade.

### v2 — Multilingual Expansion

```
Arabic foundation (translated + reviewed core pages)
Chinese foundation
Japanese foundation
French foundation
German foundation
Spanish foundation
```

Purpose: multiply authority across language editions without duplicating quality failures.

Rule: no language edition may go live until every page in that edition passes the quality gate.

### v3 — Large-Scale Topical Graph

```
10,000–50,000 pages
Full glossary (2,000+ terms)
Full question bank (5,000+ questions)
Full country registry
Full use-case matrix
Full source brief library
Full claim review library
```

Purpose: become the sovereign reference authority for SBSP and orbital energy infrastructure globally.

---

## Quality Rules for Seed Pack Data

### Glossary Terms

- Each term must have a definition of at least 100 words.
- Each term must have a `claimBoundary` statement.
- Each term must link to at least one reference page.
- No term may contain certainty language without a source citation.
- No AI-generated filler definitions allowed.

### Question Pages

- Each question must have a substantive answer of at least 150 words.
- Each question must have an `answerBoundary` statement.
- Each question must link to at least one source-backed reference page.
- Questions must not promise commercial timelines without source citation.

### Program Profiles

- Each program entry must have a verifiable `institution` name.
- Each program must have a `claimBoundary` explaining what the profile does and does not prove.
- Status must be one of the approved values: `active | concluded | announced | research_phase | demonstration_phase | commercial_phase`.
- No program profile may claim commercial deployment without a specific source citation.

---

## Data File Locations

```
main/data/glossary_terms.json     — 30 terms (v1A)
main/data/question_bank.json      — 25 questions (v1A)
main/data/program_registry.json   — 10 programs (v1A)
main/data/comparison_matrix.json  — 10 comparisons (v1A, planned)
main/data/audience_guides.json    — 8 guides (v1A, planned)
main/data/use_case_registry.json  — seeded in v1A
```

---

## Success Criteria for v1A

The Seed Pack v1A is considered successful when:

1. All data files pass the full quality gate.
2. `build.py` generates all 84 pages without error.
3. `sitemap.xml` or `sitemap_index.xml` includes exactly the approved URLs.
4. No orphan pages exist in `public/`.
5. `robots.txt` is correctly generated.
6. GitHub Actions CI is green.
7. The PR from the engine branch merges cleanly into `main`.

After v1A success, the project transitions to v1B expansion planning.
