# Data Model

## Purpose

This document defines the sovereign data layer for Space-Based-Solar-Power.com.

The data layer is the true intelligence of the asset. Pages are outputs. Data is the source. Every expansion — from a single glossary term to a country profile to a claim review — originates in a structured data file, not in a manually created content file.

---

## Data File Registry

| File | Role | Scale Target |
|---|---|---|
| `main/data/pages.json` | Master page registry, statuses, metadata | All pages |
| `main/data/navigation.json` | Approved public navigation structure | Fixed |
| `main/data/ontology.json` | Concept graph, entities, relationships, domains | ~2,000 nodes |
| `main/data/page_blueprints.json` | Required structure per page type | ~20 blueprints |
| `main/data/topic_clusters.json` | SEO cluster groupings | ~50 clusters |
| `main/data/source_claims.json` | Source registry and claim boundaries | ~500–5,000 |
| `main/data/internal_link_graph.json` | Link rules per page type and node | Full graph |
| `main/data/glossary_terms.json` | Glossary entries with definitions and links | 500–2,000 |
| `main/data/program_registry.json` | Institutional programs and projects | 100–1,000 |
| `main/data/question_bank.json` | Long-tail question pages | 1,000–5,000 |
| `main/data/comparison_matrix.json` | Structured comparison entries | 500–2,000 |
| `main/data/audience_guides.json` | Audience-specific entry paths | ~20 |
| `main/data/country_registry.json` | Country and region profiles | 300–2,000 |
| `main/data/use_case_registry.json` | Use-case profiles | 500–3,000 |

---

## Schema: pages.json

The master registry. Every page that may ever exist in the asset must have an entry here.

```json
{
  "asset": {
    "domain": "string",
    "repository": "string",
    "sourceLanguage": "string",
    "defaultLocale": "string",
    "title": "string",
    "positioning": "string",
    "launchModel": "string"
  },
  "publicationStatuses": {},
  "languages": {},
  "pages": [
    {
      "id": "string (unique)",
      "slug": "string",
      "path": "string (absolute, trailing slash)",
      "type": "string (must match page_blueprints.json)",
      "template": "string",
      "status": "string (must match publicationStatuses)",
      "phase": "string",
      "sitemap": "boolean",
      "navigation": "boolean",
      "priority": "number (0.0–1.0)",
      "changefreq": "string",
      "primaryAudience": ["string"],
      "title": "string",
      "description": "string (50–160 chars)",
      "primarySeoCluster": ["string"],
      "strategicRole": "string",
      "requiredInternalLinks": ["string (absolute paths)"],
      "sourceBoundary": "string"
    }
  ],
  "localizedCandidates": []
}
```

**Required fields for every page entry:**
- `id` — unique across all pages
- `slug` — URL-safe, no spaces
- `path` — absolute path with trailing slash
- `type` — must exist in `page_blueprints.json`
- `template` — must exist as a template file
- `status` — must match a key in `publicationStatuses`
- `sitemap` — explicit boolean
- `navigation` — explicit boolean
- `title` — unique, non-empty
- `description` — 50–160 characters
- `requiredInternalLinks` — minimum 2 entries for non-gateway pages

---

## Schema: ontology.json

The concept graph. Defines the knowledge structure of the entire domain.

```json
{
  "version": "string",
  "domain": "space-based-solar-power",
  "nodes": [
    {
      "id": "string (unique)",
      "label": "string",
      "type": "concept | technology | institution | constraint | use_case | region | person | standard",
      "domain": "string (sub-domain)",
      "aliases": ["string"],
      "definition": "string",
      "status": "established | emerging | proposed | deprecated",
      "sourceBoundary": "string",
      "relatedNodes": ["string (node ids)"],
      "parentNode": "string | null",
      "pageRef": "string | null (path to page if one exists)"
    }
  ],
  "relationships": [
    {
      "from": "string (node id)",
      "to": "string (node id)",
      "type": "is_part_of | enables | constrains | depends_on | competes_with | is_variant_of | is_used_in",
      "strength": "strong | moderate | weak",
      "sourceRef": "string | null"
    }
  ]
}
```

---

## Schema: page_blueprints.json

Defines the required structure for every page type. The build system enforces these blueprints. The validation system rejects pages that violate them.

```json
{
  "blueprints": {
    "glossary_term": {
      "requiredFields": ["id", "term", "definition", "domain", "relatedTerms", "sourceRef", "pageLinks"],
      "requiredSections": ["definition", "context", "constraints", "related", "sources"],
      "minContentLength": 300,
      "maxContentLength": 3000,
      "seoRequirements": {
        "titlePattern": "{term} — SBSP Glossary",
        "descriptionMin": 50,
        "descriptionMax": 160,
        "requireH1": true,
        "requireCanonical": true
      },
      "linkRequirements": {
        "minInternalLinks": 3,
        "requireParentHub": true,
        "requireTrustPage": true
      }
    },
    "question_answer": {
      "requiredFields": ["id", "question", "answer", "category", "relatedQuestions", "sourceBoundary", "pageLinks"],
      "requiredSections": ["answer", "context", "constraints", "related"],
      "minContentLength": 400,
      "maxContentLength": 5000,
      "seoRequirements": {
        "titlePattern": "{question}",
        "descriptionMin": 50,
        "descriptionMax": 160,
        "requireH1": true,
        "requireCanonical": true
      },
      "linkRequirements": {
        "minInternalLinks": 3,
        "requireParentHub": true,
        "requireTrustPage": true,
        "requireNextStep": true
      }
    },
    "comparison_page": {
      "requiredFields": ["id", "subjectA", "subjectB", "dimensions", "verdict", "sourceBoundary"],
      "requiredSections": ["overview", "dimension_comparison", "constraints", "claim_boundary", "related"],
      "minContentLength": 600,
      "seoRequirements": {
        "requireH1": true,
        "requireCanonical": true
      },
      "linkRequirements": {
        "minInternalLinks": 4,
        "requireParentHub": true,
        "requireTrustPage": true
      }
    },
    "country_profile": {
      "requiredFields": ["id", "country", "region", "sbspRelevance", "institutionalActivity", "sourceBoundary", "claimBoundary"],
      "requiredSections": ["overview", "institutional_activity", "strategic_context", "constraints", "sources"],
      "minContentLength": 500,
      "seoRequirements": {
        "requireH1": true,
        "requireCanonical": true
      },
      "linkRequirements": {
        "minInternalLinks": 4,
        "requireTrustPage": true
      }
    },
    "program_profile": {
      "requiredFields": ["id", "programName", "institution", "country", "status", "description", "sourceBoundary", "sourceRef"],
      "requiredSections": ["overview", "program_details", "current_status", "claim_boundary", "sources"],
      "minContentLength": 400,
      "seoRequirements": {
        "requireH1": true,
        "requireCanonical": true
      },
      "linkRequirements": {
        "minInternalLinks": 3,
        "requireParentHub": "/global-programs/",
        "requireTrustPage": true
      }
    },
    "use_case_profile": {
      "requiredFields": ["id", "useCase", "domain", "sbspFit", "constraints", "sourceBoundary"],
      "requiredSections": ["overview", "sbsp_fit", "constraints", "claim_boundary", "related"],
      "minContentLength": 350,
      "seoRequirements": {
        "requireH1": true,
        "requireCanonical": true
      },
      "linkRequirements": {
        "minInternalLinks": 3,
        "requireTrustPage": true
      }
    },
    "constraint_page": {
      "requiredFields": ["id", "constraint", "domain", "severity", "description", "sourceBoundary", "claimBoundary"],
      "requiredSections": ["constraint_statement", "technical_context", "current_status", "claim_boundary", "sources"],
      "minContentLength": 400,
      "seoRequirements": {
        "requireH1": true,
        "requireCanonical": true
      },
      "linkRequirements": {
        "minInternalLinks": 3,
        "requireParentHub": "/feasibility-and-constraints/",
        "requireTrustPage": true
      }
    },
    "source_brief": {
      "requiredFields": ["id", "sourceTitle", "sourceType", "institution", "year", "summary", "claimsExtracted", "claimBoundary"],
      "requiredSections": ["source_summary", "key_claims", "claim_boundaries", "related_pages"],
      "minContentLength": 300,
      "seoRequirements": {
        "requireH1": true,
        "requireCanonical": true
      },
      "linkRequirements": {
        "minInternalLinks": 3,
        "requireParentHub": "/sources/",
        "requireTrustPage": true
      }
    },
    "audience_guide": {
      "requiredFields": ["id", "audience", "primaryNeeds", "recommendedPages", "tools", "warnings"],
      "requiredSections": ["audience_context", "recommended_path", "tools", "important_boundaries"],
      "minContentLength": 300,
      "seoRequirements": {
        "requireH1": true,
        "requireCanonical": true
      },
      "linkRequirements": {
        "minInternalLinks": 4,
        "requireTrustPage": true
      }
    }
  }
}
```

---

## Schema: source_claims.json

```json
{
  "sources": [
    {
      "id": "string (unique)",
      "title": "string",
      "type": "institutional | academic | enterprise | government | media | ngo",
      "institution": "string",
      "year": "number",
      "url": "string | null",
      "doi": "string | null",
      "tier": 1,
      "summary": "string",
      "claims": [
        {
          "claimId": "string",
          "statement": "string",
          "type": "technical | economic | strategic | regulatory | safety",
          "boundary": "verified | disputed | preliminary | interpreted | speculative",
          "pageRefs": ["string (paths)"]
        }
      ]
    }
  ]
}
```

---

## Schema: internal_link_graph.json

See `INTERNAL_LINK_GRAPH_POLICY.md` for the full policy. The schema is:

```json
{
  "version": "string",
  "rules": [
    {
      "pageType": "string",
      "parentHub": "string (path)",
      "requiredLinks": ["string (paths)"],
      "conditionalLinks": [
        {
          "condition": "string",
          "link": "string (path)"
        }
      ],
      "trustPage": "string (path)",
      "nextStepPage": "string (path)"
    }
  ],
  "hubDefinitions": {
    "/": {"role": "primary_gateway", "maxOutboundLinks": 20},
    "/framework/": {"role": "central_hub", "maxOutboundLinks": 40},
    "/methodology/": {"role": "trust_hub", "maxOutboundLinks": 30},
    "/sources/": {"role": "source_hub", "maxOutboundLinks": 50},
    "/feasibility-and-constraints/": {"role": "credibility_hub", "maxOutboundLinks": 50},
    "/global-programs/": {"role": "registry_hub", "maxOutboundLinks": 100},
    "/tools/": {"role": "tools_hub", "maxOutboundLinks": 30},
    "/glossary/": {"role": "glossary_hub", "maxOutboundLinks": 200}
  }
}
```

---

## Schema: glossary_terms.json

```json
{
  "terms": [
    {
      "id": "string",
      "term": "string",
      "slug": "string",
      "path": "/glossary/{slug}/",
      "domain": "technical | strategic | economic | institutional | regulatory",
      "definition": "string (100–500 words)",
      "shortDefinition": "string (1–2 sentences)",
      "relatedTerms": ["string (slugs)"],
      "parentConcept": "string (ontology node id) | null",
      "sourceRef": "string (source id) | null",
      "claimBoundary": "string",
      "pageLinks": ["string (paths)"],
      "status": "approved | draft | review",
      "sitemap": "boolean",
      "seoTitle": "string",
      "seoDescription": "string"
    }
  ]
}
```

---

## Schema: question_bank.json

```json
{
  "questions": [
    {
      "id": "string",
      "question": "string",
      "slug": "string",
      "path": "/questions/{slug}/",
      "category": "technical | strategic | economic | regulatory | general",
      "answer": "string",
      "answerBoundary": "string",
      "relatedQuestions": ["string (slugs)"],
      "pageLinks": ["string (paths)"],
      "sourceRef": "string | null",
      "status": "approved | draft",
      "sitemap": "boolean",
      "seoTitle": "string",
      "seoDescription": "string"
    }
  ]
}
```

---

## Schema: program_registry.json

```json
{
  "programs": [
    {
      "id": "string",
      "programName": "string",
      "slug": "string",
      "path": "/programs/{slug}/",
      "institution": "string",
      "institutionType": "government | academic | commercial | ngo | intergovernmental",
      "country": "string",
      "startYear": "number | null",
      "status": "active | concluded | announced | research_phase | demonstration_phase | commercial_phase",
      "sbspFocus": "string",
      "description": "string",
      "claimBoundary": "string",
      "sourceRef": ["string (source ids)"],
      "pageLinks": ["string (paths)"],
      "sitemap": "boolean",
      "seoTitle": "string",
      "seoDescription": "string"
    }
  ]
}
```

---

## Anti-Pattern Rules

The following data patterns are rejected by the validation system:

| Pattern | Validator | Result |
|---|---|---|
| Empty `definition` in glossary term | `validate_schema.py` | FAIL |
| `answer` under 100 chars in question | `validate_content.py` | FAIL |
| `sourceRef: null` on technical claim | `validate_claims.py` | FAIL |
| `sitemap: true` on `status: draft` page | `validate_sitemap.py` | FAIL |
| Duplicate `slug` values | `validate_duplicates.py` | FAIL |
| `pageLinks` pointing to non-existent path | `validate_links.py` | FAIL |
| `claimBoundary` missing on constraint page | `validate_claims.py` | FAIL |
| `seoDescription` over 160 chars | `validate_seo.py` | FAIL |
