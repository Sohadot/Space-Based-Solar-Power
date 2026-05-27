# Publication Trial v1A Plan

## Purpose

Publication Trial v1A is the first controlled generation test for the Sovereign Generation Engine v1.

The Sovereign Quality Gate passed on `main` (2026-05-27), confirming that the build pipeline, validators, sitemap logic, SEO checks, source validation, claim boundaries, post-build link validation, and internal-link graph validation operate together without blocking errors.

Publication Trial v1A is **not** bulk expansion. It is a proof that the engine can produce real generated pages — from seed data, through the full validator stack, into `public/` and `sitemap.xml` — without breaking any governance rule.

Passing this trial is the gating condition for Publication Expansion v1B (300–500 pages).

---

## Selected Pages

### Glossary — 10 pages

| Seed ID | Path |
|---------|------|
| space-based-solar-power | /glossary/space-based-solar-power/ |
| solar-power-satellite | /glossary/solar-power-satellite/ |
| wireless-power-transmission | /glossary/wireless-power-transmission/ |
| microwave-power-beaming | /glossary/microwave-power-beaming/ |
| laser-power-transmission | /glossary/laser-power-transmission/ |
| rectenna | /glossary/rectenna/ |
| geostationary-orbit | /glossary/geostationary-orbit/ |
| orbital-assembly | /glossary/orbital-assembly/ |
| energy-sovereignty | /glossary/energy-sovereignty/ |
| grid-resilience | /glossary/grid-resilience/ |

All IDs confirmed present in `main/data/glossary_terms.json`. No substitutions required.

### Questions — 8 pages

| Requested ID | Actual Seed ID | Path | Notes |
|---|---|---|---|
| what-is-space-based-solar-power | what-is-space-based-solar-power | /questions/what-is-space-based-solar-power/ | Exact match |
| how-does-space-based-solar-power-work | how-does-space-based-solar-power-work | /questions/how-does-space-based-solar-power-work/ | Exact match |
| is-space-based-solar-power-possible | what-is-trl-sbsp | /questions/technology-readiness-level-sbsp/ | **Substitution**: No question with ID `is-space-based-solar-power-possible` exists. `what-is-trl-sbsp` covers SBSP technical feasibility and readiness with full answerBoundary. |
| is-space-based-solar-power-safe | what-is-sbsp-safety | /questions/is-space-based-solar-power-safe/ | ID differs from slug; seed ID is `what-is-sbsp-safety` |
| how-large-would-a-rectenna-be | what-is-rectenna-footprint-question | /questions/how-large-rectenna-for-sbsp/ | **Substitution**: No question with ID `how-large-would-a-rectenna-be` exists. `what-is-rectenna-footprint-question` (slug: `how-large-rectenna-for-sbsp`) is the existing equivalent. |
| why-is-sbsp-not-commercial-yet | why-is-sbsp-not-commercially-deployed | /questions/why-is-sbsp-not-commercially-deployed/ | **Substitution**: No question with ID `why-is-sbsp-not-commercial-yet` exists. `why-is-sbsp-not-commercially-deployed` is the existing equivalent. |
| what-are-the-main-sbsp-constraints | what-are-the-main-sbsp-constraints | /questions/what-are-the-main-sbsp-constraints/ | Exact match |
| who-is-working-on-space-based-solar-power | which-countries-research-sbsp | /questions/which-countries-research-sbsp/ | **Substitution**: No question with that ID exists. `which-countries-research-sbsp` is the strongest available equivalent covering all major SBSP research programs. |

### Programs — 5 pages

| Requested ID | Actual Seed ID | Path | Notes |
|---|---|---|---|
| nasa-space-based-solar-power | nasa-space-solar-power-revisit | /programs/nasa-space-solar-power-revisit/ | **Substitution**: Actual ID in program_registry.json is `nasa-space-solar-power-revisit`. Covers NASA 1979 Reference Study and modern assessments with full claimBoundary and sourceRef. |
| esa-solaris | esa-solaris | /programs/esa-solaris/ | Exact match |
| jaxa-ssps | jaxa-ssps | /programs/jaxa-ssps/ | Exact match |
| caltech-space-solar-power-project | caltech-sspp | /programs/caltech-sspp/ | **Substitution**: Actual ID is `caltech-sspp`. Covers the Caltech SSPP including MAPLE orbital demonstration with full claimBoundary and sourceRef. |
| uk-space-based-solar-power | uk-space-energy-initiative | /programs/uk-space-energy-initiative/ | **Substitution**: No program with ID `uk-space-based-solar-power` exists. `uk-space-energy-initiative` has strong sourceRef and explicit claimBoundary. Selected over `china-sbsp-programme` because source boundary is clearer and more consistently verifiable from open sources. |

---

## Publication Eligibility Rules

A seed item is eligible for publication in this trial if:

1. Its ID is listed in `main/data/publication_trial_v1a.json`.
2. The item exists in the corresponding seed file (`glossary_terms.json`, `question_bank.json`, or `program_registry.json`).
3. Required schema fields are present and non-empty.
4. A `claimBoundary` or `answerBoundary` field is present and non-empty.
5. The corresponding page entry in `pages.json` has `status: "approved_for_launch"`.
6. The page passes all validators in the quality gate.

---

## Sitemap Eligibility Rules

A generated page is eligible for the sitemap if:

1. Its `pages.json` entry has `sitemap: true`.
2. It was successfully generated into `public/`.
3. It passes post-build SEO validation (title ≤70 chars, description 50–160 chars, H1 present, canonical present).
4. It passes post-build link validation (no broken internal links).

Seed-only items (items in seed files but not in the trial manifest) are **not** sitemap eligible and must not appear in `sitemap.xml`.

---

## Internal Link Requirements

Every generated trial page must satisfy:

- **Parent hub link**: each glossary term links to `/glossary/`; each question links to `/what-is-space-based-solar-power/`; each program links to `/global-programs/`.
- **Trust link**: every page must link to `/methodology/` or `/sources/`.
- **At least 2 related links**: cross-links to other trial pages where applicable.
- **Next-step link**: at least one link to a core reference page (`/feasibility-and-constraints/`, `/framework/`, `/sources/`).
- **No orphan status**: every page must have at least 1 inbound link from another approved page.

Hub pages (`/glossary/`, `/questions/`, `/programs/`) must link to all trial pages within their category.

---

## sourceBoundary Requirements

- Glossary terms may have `sourceRef: null` because they define established concepts and explicitly state claim boundaries.
- Questions have `answerBoundary` which serves the claim discipline function.
- Program profiles must have `sourceRef` arrays with institutional source identifiers and explicit `claimBoundary` fields.
- No program profile may be published without at least one `sourceRef` entry and a non-empty `claimBoundary`.

---

## claimBoundary Requirements

- Every glossary term must have a non-empty `claimBoundary` field.
- Every question must have a non-empty `answerBoundary` field.
- Every program profile must have a non-empty `claimBoundary` field.
- No certainty claim (e.g., "SBSP will be deployed", "SBSP is economically viable") may appear without explicit qualification.

---

## No-Thin-Content Rule

- Glossary definitions must be ≥100 characters (enforced by `validate_content.py`).
- Question answers must be ≥100 characters (enforced by `validate_schema.py`).
- Program descriptions must be substantive (≥100 characters, full institutional context).
- Hub pages must list real generated items, not empty placeholders.

---

## No-Orphan-Pages Rule

Every `approved_for_launch` page must have at least 1 inbound link from another approved page. Enforced by `validate_internal_link_graph.py`.

Resolution:
- Trial glossary terms are linked from the `/glossary/` hub page.
- Trial question pages are linked from the `/questions/` hub page.
- Trial program pages are linked from both the `/programs/` hub and the updated `/global-programs/` page.
- Hub pages (`/glossary/`, `/questions/`, `/programs/`) are linked from the home page.

---

## No-Fake-Profile Rule

No program profile may be invented or fabricated. All profiles must:

- Have a real institutional entity as `institution`.
- Have a real published `sourceRef` (institutional documents, government studies, or academic papers).
- Have a `claimBoundary` that correctly describes what is and is not known about the programme.
- Not claim deployment, funding commitment, or commercial capability that is not documented in the source references.

---

## Acceptance Criteria

Publication Trial v1A passes when:

1. CI is fully green on the feature branch.
2. `public/` contains the 23 trial pages plus 3 hub pages (plus all existing approved pages).
3. `sitemap.xml` or `sitemap_index.xml` contains only generated, eligible pages.
4. No orphan pages exist in the generated output.
5. No broken internal links in any generated HTML file.
6. No `sourceRef` is missing on program profiles.
7. No claims appear without a corresponding `claimBoundary` or `answerBoundary`.
8. No thin content — all definitions, answers, and descriptions meet minimum length requirements.
9. All generated HTML files pass SEO validation (title ≤70 chars, description 50–160 chars, H1, canonical).
10. Internal link graph passes: all hubs within budget, all required links present, no orphan pages.

---

## Next Stage

After Publication Trial v1A passes:

**Publication Expansion v1B** — 300–500 pages across glossary, questions, programs, comparisons, and audience guides.

Expansion remains blocked until v1A demonstrates that the engine produces high-quality, validator-approved, sitemap-eligible reference pages at trial scale.
