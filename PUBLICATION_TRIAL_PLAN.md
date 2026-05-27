# Publication Trial v1A — Plan

**Status:** Approved  
**Phase:** publication_trial_v1a  
**Date:** 2026-05-27  
**Engine:** Sovereign Generation Engine v1  

---

## Purpose

Publication Trial v1A is the first controlled publication test for the Sovereign Generation Engine v1. The pipeline passed the full quality gate on `main`. This trial generates 23 real reference pages from seed data through the full validator stack into `public/` and `sitemap.xml`.

This is not a random page addition. It is not a scaled expansion. It is a disciplined first test of the generation path: seed data → pages.json → build.py → quality gate → public/.

---

## Selection Rules

1. Only pages explicitly listed in `publication_trial_v1a.json` are generated in this trial.
2. All pages must pass the full quality gate: schema, content, links, sources, claims, SEO, sitemap, internal link graph.
3. No placeholder pages. No thin content. No fake profiles.
4. No weakening of any validator for this trial.
5. No bypass of quality gates.
6. All selected seed IDs must exist in seed data files. If a requested ID does not exist, a documented substitution is required.

---

## Pages Selected

### Glossary Terms (10)
Pages generated from `main/data/glossary_terms.json`:

| Page ID | Seed ID | Path |
|---|---|---|
| gterm-sbsp | space-based-solar-power | /glossary/space-based-solar-power/ |
| gterm-sps | solar-power-satellite | /glossary/solar-power-satellite/ |
| gterm-wpt | wireless-power-transmission | /glossary/wireless-power-transmission/ |
| gterm-microwave | microwave-power-beaming | /glossary/microwave-power-beaming/ |
| gterm-laser | laser-power-transmission | /glossary/laser-power-transmission/ |
| gterm-rectenna | rectenna | /glossary/rectenna/ |
| gterm-geo | geostationary-orbit | /glossary/geostationary-orbit/ |
| gterm-launch-economics | launch-economics | /glossary/launch-economics/ |
| gterm-energy-sovereignty | energy-sovereignty | /glossary/energy-sovereignty/ |
| gterm-trl | technology-readiness-level | /glossary/technology-readiness-level/ |

### Question Pages (8)
Pages generated from `main/data/question_bank.json`:

| Page ID | Seed ID | Path |
|---|---|---|
| q-what-is-sbsp | what-is-space-based-solar-power | /questions/what-is-space-based-solar-power/ |
| q-how-sbsp-works | how-does-space-based-solar-power-work | /questions/how-does-space-based-solar-power-work/ |
| q-sbsp-not-deployed | why-is-sbsp-not-commercially-deployed | /questions/why-is-sbsp-not-commercially-deployed/ |
| q-sbsp-constraints | what-are-the-main-sbsp-constraints | /questions/what-are-the-main-sbsp-constraints/ |
| q-what-is-rectenna | what-is-a-rectenna | /questions/what-is-a-rectenna/ |
| q-microwave-vs-laser | what-is-microwave-vs-laser-beaming | /questions/what-is-microwave-vs-laser-beaming/ |
| q-which-countries | which-countries-research-sbsp | /questions/which-countries-research-sbsp/ |
| q-esa-solaris | what-is-esa-solaris | /questions/what-is-esa-solaris/ |

### Program Profiles (5)
Pages generated from `main/data/program_registry.json`:

| Page ID | Seed ID | Path |
|---|---|---|
| prog-esa-solaris | esa-solaris | /programs/esa-solaris/ |
| prog-jaxa-ssps | jaxa-ssps | /programs/jaxa-ssps/ |
| prog-nasa-revisit | nasa-space-solar-power-revisit | /programs/nasa-space-solar-power-revisit/ |
| prog-caltech-sspp | caltech-sspp | /programs/caltech-sspp/ |
| prog-uk-sei | uk-space-energy-initiative | /programs/uk-space-energy-initiative/ |

### Hub Pages (3)
Hub pages upgraded or created to serve as parent indexes:

| Page ID | Path | Action |
|---|---|---|
| glossary | /glossary/ | Upgraded from expansion_cluster_2 to approved_for_launch |
| questions | /questions/ | New hub page added |
| programs | /programs/ | New hub page added |

---

## Substitutions

None. All selected IDs are present in their respective seed data files.

---

## Sitemap Eligibility

Sitemap inclusion requires `sitemap: true` in pages.json. Rules applied:
- Hub pages (`/glossary/`, `/questions/`, `/programs/`): `sitemap: true`
- Glossary term pages: `sitemap: true`
- Question pages: `sitemap: true`
- Program profile pages: `sitemap: true`

---

## Internal Link Requirements

Each generated page must have at least the following inbound links to prevent orphan errors:
- Glossary terms: inbound from `/glossary/` hub (required)
- Question pages: inbound from `/questions/` hub (required)
- Program pages: inbound from `/programs/` hub and `/global-programs/` (required)
- Hub pages: inbound from `/` home page (required)

Each generated page must include in `requiredInternalLinks`:
- Glossary terms: `/glossary/` (parent hub) + `/sources/` (trust)
- Question pages: `/methodology/` (trust + required by type rule)
- Program pages: `/global-programs/` + `/sources/` (required by type rule) + `/methodology/` (trust)

---

## Source and Claim Boundary Requirements

- All glossary terms have `claimBoundary` fields in seed data. These are included in generated HTML.
- All question pages have `answerBoundary` fields in seed data. These are included in generated HTML.
- All program profiles have `claimBoundary` fields in seed data. These map to `sourceBoundary` in pages.json entries (required for `program_profile` type by validate_claims.py and validate_sources.py).
- Programs with `sourceRef: null` are excluded from this trial. All 5 selected programs have explicit `sourceRef` arrays.

---

## No-Thin-Content Rule

Content requirements enforced before publication:
- Glossary definitions: ≥100 characters (enforced by validate_content.py). All 10 selected terms have definitions of 450+ characters.
- Question answers: substantive, multi-sentence answers from seed data.
- Program descriptions: institutional descriptions of 500+ characters from seed data.

---

## No-Fake-Profile Rule

All 5 program profiles selected are documented real institutional programs with published sourceRef entries:
- ESA SOLARIS: real ESA initiative, sourceRef present
- JAXA SSPS: real JAXA programme, sourceRef present
- NASA Space Solar Power: real NASA programme history, sourceRef present
- Caltech SSPP: real Caltech project, sourceRef present
- UK Space Energy Initiative: real UK industry consortium, sourceRef present

---

## Acceptance Criteria

- [ ] CI quality gate passes on `claude/publication-trial-v1a-P8gpb`
- [ ] 23 content pages + 3 hub pages generated in `public/`
- [ ] Sitemap contains all 26 new pages
- [ ] No orphan pages (every approved page has ≥1 inbound link)
- [ ] No broken links in generated HTML
- [ ] No missing sourceBoundary on program_profile pages
- [ ] No dangerous certainty claims without boundaries
- [ ] No thin content (all definitions ≥100 chars, all answers substantive)
- [ ] All page titles ≤70 chars, descriptions 50-160 chars
- [ ] Canonical URLs correct in all generated HTML
- [ ] Exactly one h1 per generated page
