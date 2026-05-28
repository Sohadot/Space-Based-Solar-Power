# V1B-D Global Programs & Institutional Activity Expansion — Sprint Plan

## Sprint Objective

Expand the /global-programs/ reference layer from 5 published program profiles into a comprehensive institutional intelligence layer of 30 governed program entries. The goal is to make the asset credible to institutional buyers by showing which agencies, research programs, national initiatives, academic programs, defense-linked studies, and private/consortium efforts are connected to space-based solar power.

## Allowed Page Types

- `programs_hub` — upgraded cluster-grouped hub at /programs/
- `program_profile` — governed program/institution profile pages at /programs/{slug}/
- `program_page` — richer profile pages using the program_pages.json schema

## Blocked Actions

- Google Search Console submission: BLOCKED until post-merge live verification
- WebGL: BLOCKED
- JavaScript-dependent interface changes: BLOCKED
- Manual public/ patching: BLOCKED
- Weakening validators: BLOCKED
- Removing, rewriting, compressing, or reordering DECISION_LOG entries: BLOCKED
- v1B-E: BLOCKED until v1B-D is merged, deployed, live-verified, and V1B-DL-009 is recorded

## Data Requirements

- program_pages.json: 30 entries minimum
- Each entry: id, slug, title, institution, country_or_region, program_status, activity_type, cluster, summary (≥150 chars), institutional_context, sbsp_relevance, technology_relationship, feasibility_boundary, claim_boundary, related_glossary_terms (≥2), related_questions (≥2), related_technology_pages (≥1 where applicable), source_footer, seoTitle, seoDescription
- No duplicate IDs or slugs
- No banned overclaim language

## Claim-Boundary Rules

No entry may claim that SBSP is:
- Commercially deployed
- Operational at utility scale
- Proven as a full infrastructure system
- Ready for immediate investment without risk

All technology readiness claims must be qualified with TRL or equivalent framing. Timeline claims from program roadmaps must be explicitly identified as planning targets, not funded commitments.

## Internal Linking Rules

- Each program page must link back to /global-programs/ and /programs/
- Each program page must link to /methodology/ and /sources/
- Each program page must link to at least 2 glossary terms
- Each program page must link to at least 2 reference questions
- Each program page must link to at least 1 technology page where a direct technology relationship exists
- Hub pages must link to all child pages they govern

## Validation Rules (validate_programs.py)

- No duplicate IDs
- No duplicate slugs
- Required fields present: id, slug, title, institution, country_or_region, program_status, activity_type, cluster, summary, institutional_context, sbsp_relevance, technology_relationship, feasibility_boundary, claim_boundary, related_glossary_terms, related_questions, source_footer, seoTitle, seoDescription
- summary minimum length: 150 characters
- institutional_context present and non-empty
- sbsp_relevance present and non-empty
- technology_relationship present and non-empty
- feasibility_boundary present and non-empty
- claim_boundary present and non-empty
- At least 2 related_glossary_terms per entry
- At least 2 related_questions per entry
- At least 1 related_technology_pages where activity_type is not historical_reference
- No banned overclaim language in summary, institutional_context, sbsp_relevance, or claim_boundary
- source_footer present and non-empty
- All linked glossary slugs resolve to known glossary terms
- All linked question IDs resolve to known questions
- All linked technology page IDs resolve to known technology pages

## Banned Overclaim Language

- "commercially deployed"
- "operational at utility scale"
- "proven infrastructure"
- "commercially viable" (without qualification)
- "ready for deployment"
- "fully demonstrated"

## Post-Merge Live Verification Requirements

1. Branch merged to main via PR
2. GitHub Pages deployment completes
3. /programs/ hub renders with cluster grouping, status panel, expansion note, cluster jump navigation, and source/methodology footer
4. All 30 program pages render with full field content
5. sitemap-programs-001.xml contains all 30 program URLs
6. sitemap.xml remains a sitemap index
7. Legacy ref-nav: 0 matches
8. No manual public/ patching detected
9. DECISION_LOG integrity: all prior IDs S1-DL-001 through V1B-DL-008 present

## v1B-E Gate

v1B-E remains BLOCKED until:
- v1B-D is merged to main
- GitHub Pages deployment confirmed live
- Post-merge live verification approved
- V1B-DL-009 recorded in DECISION_LOG

## Program Clusters

1. national-space-agency — National Space Agency Programs
2. national-research-program — National Research and Industrial Programs
3. defense-military — Defense and Military Research
4. academic-university — Academic and University Programs
5. industry-consortium — Industry and Consortium Programs
6. historical-foundational — Historical and Foundational References
