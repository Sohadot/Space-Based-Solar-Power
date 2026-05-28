# V1B Questions Expansion Plan — Sprint v1B-B

## 1. Purpose of v1B-B

v1B-B is the second controlled content expansion cluster for Space-Based-Solar-Power.com. Its scope is the question layer: expanding the existing 8 published questions into a substantive governed Q&A reference layer of 50+ questions across 7 question clusters.

The question layer is the primary organic search surface. People searching for SBSP are asking questions. The glossary layer from v1B-A defines the vocabulary. The question layer provides the first-level answers — with source discipline, claim boundaries, and internal links to the terminology and reference infrastructure.

## 2. Why Questions Come After Glossary

The glossary established the terminology foundation: precise definitions for 53 key concepts, each claim-boundary controlled. The question layer builds on that foundation:

- Questions must link to glossary terms they reference.
- Questions inherit the same claim discipline — no answer may assert SBSP is deployed or proven commercially.
- Questions are higher-intent search queries than glossary term lookups.
- A strong Q&A layer makes the asset legible to general audiences as well as technical ones.

## 3. Target Count

- New questions this sprint: ~30
- Total published after v1B-B: 50–56
- All from the seven governed clusters defined below
- No random question addition — every question must map to a cluster

## 4. Required Question Fields

Each question in `main/data/question_bank.json` must include:

| Field | Requirement |
|---|---|
| `id` | Unique, slug-format string |
| `question` | Full question text, ending with `?` |
| `slug` | URL-safe version |
| `path` | `/questions/{slug}/` |
| `cluster` | One of the seven governed clusters |
| `answer` | Minimum 100 words. No placeholder text. No AI filler. Factually bounded. |
| `answerBoundary` | Explicit statement separating established knowledge from unproven claims |
| `relatedQuestions` | Array of ≥2 existing or sibling question IDs |
| `pageLinks` | Array of ≥2 approved page paths |
| `status` | `approved` for publication-ready questions |
| `sitemap` | `false` in source data (sitemap driven by pages.json) |
| `seoTitle` | ≤70 chars |
| `seoDescription` | 50–160 chars |

## 5. Source and Claim Boundary Requirements

Every question must carry an `answerBoundary` that:

1. Identifies what is established in the literature or demonstrated in research.
2. Explicitly states what has NOT been commercially deployed, proven at scale, or operationally demonstrated.
3. Does not present research-phase concepts as operational facts.

Forbidden claim patterns:
- Asserting SBSP is "deployed", "operational", or "commercially available"
- Presenting demonstration results as full-scale readiness
- Omitting that no commercial system exists

## 6. Seven Governed Clusters

### Cluster 1: Foundational (`foundational`)
Core definitional and conceptual questions about what SBSP is, how it differs from other energy sources, and why it matters.

### Cluster 2: Technology (`technology`)
Questions about the technical systems, components, and mechanisms of SBSP including orbital systems, power beaming, and ground reception.

### Cluster 3: Feasibility and Constraints (`feasibility-constraints`)
Questions about the barriers to SBSP deployment: economics, mass-to-orbit, orbital assembly, specific mass, and readiness levels.

### Cluster 4: Safety and Regulation (`safety-regulation`)
Questions about the safety, spectrum, regulatory, land footprint, and public acceptance constraints on SBSP.

### Cluster 5: Grid and Energy Systems (`grid-energy-systems`)
Questions about how SBSP would interact with terrestrial energy systems, baseload provision, remote power, and grid resilience.

### Cluster 6: AI, Defense, and Strategic Demand (`ai-defense-strategic`)
Questions about the demand-side drivers for SBSP: hyperscale AI power, defense energy resilience, cislunar operations, and space industrial demand.

### Cluster 7: Programs and Institutions (`program-institutional`)
Questions about the institutional programs, national initiatives, and historical studies of SBSP.

## 7. Internal Linking Rules

All new question pages must:

- Include `/questions/` in `requiredInternalLinks`
- Include `/sources/` in `requiredInternalLinks`
- Include at least one glossary term link relevant to the question topic
- Include at least one foundation or cluster page
- Not be orphaned: the questions hub must include their path in `requiredInternalLinks`
- Not self-link or create circular dependency

## 8. Hub Upgrade Requirements

The `/questions/` hub must be upgraded to:

- Show a status panel: total questions, clusters, claim-boundary controlled
- Show a cluster jump/index navigation
- Group questions by cluster with labelled headings
- Show an expansion note explaining the layer has grown beyond the initial seed

## 9. Quality Gate Requirements

A new `validate_questions.py` validator will be added as the 12th validator:

- Question missing answer → FAIL
- Question missing answerBoundary → FAIL
- Question missing relatedQuestions (fewer than 2) → FAIL
- Question missing pageLinks → FAIL
- Duplicate question IDs or slugs → FAIL

## 10. Publication Criteria

A question may be published only when:

1. All required fields are present and substantive
2. The question passes `validate_questions.py`
3. The full quality gate (12/12) passes
4. The question has at least 2 `relatedQuestions` that exist
5. The question has at least 2 `pageLinks` pointing to approved pages
6. The question has a non-trivial `answerBoundary`
7. No duplicate ID or slug exists in the data

## 11. Blocked Actions

- Google Search Console submission: BLOCKED
- WebGL or JavaScript-dependent interface changes: BLOCKED
- Manual patching of `public/`: BLOCKED
- Weakening or bypassing any validator: BLOCKED
- Publishing questions with placeholder answers: BLOCKED
- Publishing questions without answerBoundary: BLOCKED

## 12. Post-v1B-B Next Steps

After v1B-B passes quality gate and is merged:

1. Verify live questions hub shows all questions grouped by cluster
2. Then begin v1B-C: Technology Reference pages
3. Google Search Console submission remains blocked until explicitly authorized

---

**Governance reference:** DECISION_LOG V1B-DL-004
**Quality gate target:** 12/12 validators
**Phase identifier:** v1b_b
**Branch:** v1b-b-questions-expansion
