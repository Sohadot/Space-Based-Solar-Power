# V1B-C Technology Reference Expansion Plan

**Sprint:** v1B-C  
**Date:** 2026-05-28  
**Status:** Approved  
**Branch:** v1b-c-technology-expansion  
**Prerequisite:** v1B-B verified live (V1B-DL-005 recorded)

---

## Objective

Build a Technology Reference layer at `/technology/` with 21 governed technology pages across 7 engineering clusters. Each page provides a technical definition, infrastructure role, subsystem relationship, feasibility boundary, and explicit claim boundary, cross-linked to published glossary terms and reference questions.

---

## Governance Constraints (Unchanged from v1B-A and v1B-B)

- Do not start Google Search Console.
- Do not add WebGL, Three.js, or JavaScript-dependent interface features.
- Do not manually patch public/.
- Do not weaken validators.
- Do not create thin or placeholder technology entries.
- DECISION_LOG is append-only.
- Do not create generic blog articles.
- Do not remove or rewrite previous DECISION_LOG entries.
- v1B-D remains blocked until v1B-C is merged, deployed, live verified, and V1B-DL-007 is recorded.

---

## Technology Reference Data Model

Each entry in `main/data/technology_pages.json` requires:

| Field | Requirement |
|---|---|
| `id` | Unique slug-style identifier |
| `title` | ≤70 chars |
| `slug` | URL slug for /technology/{slug}/ |
| `path` | Full path: /technology/{slug}/ |
| `cluster` | One of 7 cluster IDs |
| `clusterLabel` | Human-readable cluster name |
| `summary` | ≥100 chars, non-placeholder technical definition |
| `infrastructureRole` | Role within the SBSP infrastructure chain |
| `subsystemRelationship` | Relationship to adjacent subsystems |
| `feasibilityBoundary` | Current TRL status and key blockers |
| `claimBoundary` | Explicit boundary: what this page claims vs. does not |
| `relatedGlossaryTerms` | ≥2 published glossary term IDs |
| `relatedQuestions` | ≥2 published question IDs |
| `pageLinks` | ≥2 internal paths (must be published routes) |
| `status` | "published" |
| `seoTitle` | ≤70 chars |
| `seoDescription` | 50–160 chars |
| `lastUpdated` | ISO date |

---

## 7 Clusters

| Cluster ID | Label | Pages |
|---|---|---|
| `photovoltaics-power-generation` | Photovoltaics and Power Generation | 3 |
| `wireless-power-transmission` | Wireless Power Transmission | 3 |
| `receiving-conversion-systems` | Receiving and Conversion Systems | 3 |
| `orbital-assembly-structures` | Orbital Assembly and Structures | 3 |
| `launch-in-space-logistics` | Launch and In-Space Logistics | 3 |
| `thermal-management-systems` | Thermal Management Systems | 3 |
| `autonomous-operations-robotics` | Autonomous Operations and Robotics | 3 |

**Total:** 21 technology reference pages

---

## Page Inventory

### Cluster 1: Photovoltaics and Power Generation
1. `/technology/high-efficiency-solar-cells/`
2. `/technology/concentrator-photovoltaics/`
3. `/technology/solar-array-structural-design/`

### Cluster 2: Wireless Power Transmission
4. `/technology/microwave-power-transmission/`
5. `/technology/laser-power-beaming/`
6. `/technology/phased-array-transmitter-systems/`

### Cluster 3: Receiving and Conversion Systems
7. `/technology/rectenna-arrays/`
8. `/technology/ground-receiving-infrastructure/`
9. `/technology/power-conversion-and-conditioning/`

### Cluster 4: Orbital Assembly and Structures
10. `/technology/in-space-assembly-methods/`
11. `/technology/modular-spacecraft-architecture/`
12. `/technology/large-space-structure-dynamics/`

### Cluster 5: Launch and In-Space Logistics
13. `/technology/heavy-lift-launch-requirements/`
14. `/technology/on-orbit-propulsion-systems/`
15. `/technology/in-space-manufacturing-systems/`

### Cluster 6: Thermal Management Systems
16. `/technology/spacecraft-thermal-control/`
17. `/technology/heat-pipe-radiator-systems/`
18. `/technology/power-electronics-thermal-management/`

### Cluster 7: Autonomous Operations and Robotics
19. `/technology/robotic-on-orbit-servicing/`
20. `/technology/autonomous-fault-detection/`
21. `/technology/coordinated-satellite-operations/`

---

## Required Internal Links (per technology page)

Each `/technology/{slug}/` page must include in `requiredInternalLinks`:
- `/technology/` — parent hub
- `/technology-stack/` — technical reference foundation page
- `/feasibility-and-constraints/` — constraint layer
- `/sources/` — source registry
- `/methodology/` — trust page
- 2× `/glossary/{slug}/` — published glossary term pages
- 2× `/questions/{slug}/` — published question pages

---

## Hub Page: /technology/

- Path: `/technology/`
- Type: `technology_index`
- Seed source: `technology_hub`
- Status panel: total pages, cluster count
- Expansion note: sprint context
- Cluster jump navigation with `id="tcluster-{cluster_id}"` anchors
- Cluster sections with page listings

---

## Validator: validate_technology.py (13th)

Checks all `technology_pages.json` entries with `status: "published"`:
- `summary` ≥100 chars, non-placeholder
- `claimBoundary` non-empty, non-placeholder
- `feasibilityBoundary` non-empty, non-placeholder
- `relatedGlossaryTerms` ≥2
- `relatedQuestions` ≥2
- `pageLinks` ≥2
- No duplicate IDs or slugs

---

## Build System Changes

- `TECH_CLUSTER_ORDER` constant added to `build.py`
- `load_trial_manifest()` updated to prefer `publication_v1b_c.json`
- `load_seed_data()` updated to load `technology_pages.json`
- `generate_technology_page_html()` added
- `generate_technology_hub_html()` added
- `write_page()` dispatch extended for `technology` and `technology_hub` seed sources
- `categorize_pages()` extended for `/technology/` paths
- `build_sitemaps()` extended to generate `sitemap-technology-001.xml`
- `internal_link_graph.json`: added `/technology/` hub definition and `technology_page` + `technology_index` rules
- `quality_gate.py`: added `validate_technology.py` as 13th validator

---

## Sitemap

- `sitemap-technology-001.xml`: 21 URLs (individual technology pages)
- `/technology/` hub: included in `sitemap-core.xml`
- Total technology-layer sitemap URLs: 22 (21 child + 1 hub in core)

---

## Delivery Checklist

- [ ] `V1B_TECHNOLOGY_EXPANSION_PLAN.md` created
- [ ] `main/data/technology_pages.json` — 21 entries, 7 clusters
- [ ] `main/data/pages.json` — 22 new entries (hub + 21 child pages)
- [ ] `main/data/publication_v1b_c.json` — v1b_c manifest
- [ ] `main/data/internal_link_graph.json` — tech hub + rules added
- [ ] `main/scripts/build.py` — tech hub/page generators + dispatch
- [ ] `main/scripts/validate_technology.py` — 13th validator
- [ ] `main/scripts/quality_gate.py` — 13th validator added
- [ ] `main/static/css/main.css` — tech hub/page CSS
- [ ] `public/` — regenerated (152 approved pages)
- [ ] `DECISION_LOG` — V1B-DL-006 prepended
- [ ] Quality gate: 13/13 PASS
- [ ] Technology sitemap: 21 URLs in sitemap-technology-001.xml
