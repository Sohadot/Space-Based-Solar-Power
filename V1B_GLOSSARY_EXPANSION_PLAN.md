# V1B Glossary Expansion Plan — Sprint v1B-A

## 1. Purpose of v1B-A

v1B-A is the first controlled content expansion cluster for Space-Based-Solar-Power.com. Its sole scope is the glossary layer: expanding the existing 10 published terms into a substantive sovereign lexical authority layer of 50+ governed terms.

v1B-A is not bulk content generation. Every term must be source-disciplined, claim-bounded, internally linked, and quality-gate approved. The purpose is to establish the terminology layer that all subsequent reference pages (technology pages, constraint pages, question pages, program profiles) will be able to cross-reference.

## 2. Why Glossary Comes First

Terminology governs the reference system. Before expanding into technology analysis, constraint pages, or audience guides, the asset must establish:

- Precise definitions for all key infrastructure, transmission, reception, grid, constraint, and strategic demand concepts.
- Consistent claim boundaries at the term level, so every page that references a term can inherit the same epistemic discipline.
- A governed SEO keyword layer — glossary terms are high-intent, definitional search queries.
- A cross-linkable internal vocabulary that every future page type can reference.

The glossary cluster comes first. Questions, technology pages, and constraint pages come after.

## 3. Target Count

- New terms this sprint: 40–50
- All from the five governed clusters defined below
- Total glossary terms after v1B-A: 50–60 published
- No random term addition — every term must map to a cluster

## 4. Required Glossary Fields

Each term in `main/data/glossary_terms.json` must include:

| Field | Requirement |
|---|---|
| `id` | Unique, slug-format string |
| `term` | Full display name |
| `slug` | URL-safe version, matches path |
| `path` | `/glossary/{slug}/` |
| `domain` | `technical`, `strategic`, or `governance` |
| `cluster` | One of the five governed clusters |
| `definition` | Minimum 3 substantive sentences. No placeholder text. No AI filler. |
| `shortDefinition` | 1 sentence, ≤120 chars |
| `relatedTerms` | Array of ≥2 existing or sibling term IDs |
| `pageLinks` | Array of ≥1 approved page paths |
| `claimBoundary` | Explicit statement separating established knowledge from unproven claims |
| `status` | `approved` for publication-ready terms |
| `sitemap` | `true` for published terms |
| `seoTitle` | ≤70 chars |
| `seoDescription` | 50–160 chars |

## 5. Source and Claim Boundary Requirements

Every glossary term must carry a `claimBoundary` that:

1. Identifies what is established in the literature or demonstrated in research.
2. Explicitly states what has NOT been commercially deployed, proven at scale, or operationally demonstrated.
3. Does not present research-phase concepts as operational facts.

Forbidden claim patterns (from `validate_claims.py`):
- Asserting SBSP is "proven", "deployed", "operational", or "commercially available"
- Presenting demonstration results as full-scale readiness
- Omitting that no commercial system exists

## 6. Internal Linking Rules

All new glossary term pages must:

- Include `/glossary/` in `requiredInternalLinks` (required by internal link graph rules for `glossary_term` type)
- Include `/sources/` in `requiredInternalLinks` (trust page requirement)
- Include at least one foundation or cluster page (`/framework/`, `/technology-stack/`, `/feasibility-and-constraints/`, `/strategic-importance/`)
- Not be orphaned: the glossary hub must include their path in its own `requiredInternalLinks`
- Not self-link or create circular dependency

Glossary hub budget: 200 outbound links maximum (current: ~13; post v1B-A: ~56).

## 7. Sitemap Eligibility Rules

A glossary term page is sitemap-eligible only when:

- `status: "approved"` in `glossary_terms.json`
- `status: "approved_for_launch"` in `pages.json`
- `sitemap: true` in both data sources
- All required fields present and passing quality gate
- Term has definition, claimBoundary, ≥2 relatedTerms, ≥1 pageLinks

## 8. Quality Gate Requirements

Quality gate (currently 10 validators) must pass with 0 failures before any publication. v1B-A adds `validate_glossary.py` making it 11 validators. The gate must pass at 11/11.

Glossary-specific failures block the build:
- Term missing definition
- Term missing claimBoundary
- Term missing relatedTerms (fewer than 2)
- Term missing pageLinks
- Duplicate term IDs or slugs
- Generated glossary page lacking source/methodology links (checked by validate_output_integrity.py)
- Glossary hub lacking child links

## 9. Publication Criteria

A term may be published (added to the v1B-A manifest and given `approved_for_launch` in pages.json) only when:

1. All required fields are present and substantive
2. The term passes `validate_glossary.py`
3. The full quality gate (11/11) passes with the term included
4. The term has at least 2 `relatedTerms` that exist in the data
5. The term has at least 1 `pageLink` pointing to an approved page
6. The term has a non-trivial `claimBoundary`
7. No duplicate ID or slug exists in the data

## 10. Blocked Actions

The following actions are prohibited until explicitly authorized by a new DECISION_LOG entry:

- Google Search Console submission
- WebGL or JavaScript-dependent interface changes
- Manual patching of any file in `public/`
- Weakening or bypassing any validator
- Random bulk term addition without cluster assignment
- Publishing terms with placeholder definitions
- Publishing terms without claimBoundary

## 11. Five Governed Clusters

### Cluster 1: Core Infrastructure
Terms defining the structural elements of SBSP as an orbital energy infrastructure system.

### Cluster 2: Transmission and Reception
Terms defining the wireless power transmission pathway from orbital transmitter to terrestrial receiver.

### Cluster 3: Grid and Energy Systems
Terms defining how SBSP interacts with terrestrial energy systems, grid demands, and power provision scenarios.

### Cluster 4: Constraints and Governance
Terms defining the technical, economic, regulatory, and social barriers to SBSP deployment.

### Cluster 5: Strategic Demand and Space Industry
Terms defining the demand-side drivers for SBSP including AI energy demand, defense resilience, and the space industrial economy.

## 12. Post-v1B-A Next Steps

After v1B-A passes quality gate and is merged:

1. Verify live glossary hub shows all terms grouped by cluster
2. Then begin v1B-B: Question Expansion (50–70 new question pages)
3. Then v1B-C: Technology Reference pages
4. Google Search Console submission remains blocked until the full v1B expansion (300–500 pages) is approved

---

**Governance reference:** DECISION_LOG V1B-DL-001  
**Quality gate target:** 11/11 validators  
**Phase identifier:** v1b_a  
**Branch:** v1b-a-glossary-expansion
