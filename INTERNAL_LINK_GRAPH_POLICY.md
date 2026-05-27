# Internal Link Graph Policy

## Purpose

This document defines the internal link graph rules for Space-Based-Solar-Power.com.

The internal link graph is not decoration. It is infrastructure.

Google uses links to understand page relationships, cluster authority, and content hierarchy. An asset with strong internal linking is more likely to be crawled efficiently, understood correctly, and indexed as a coherent topical authority.

This policy prevents:

- orphan pages (pages with no inbound links);
- dead-end pages (pages with no outbound links);
- broken link chains;
- hub pages that link to nothing;
- expansion pages that never connect to the core;
- sitemap-only discoverability (which is weaker than link-graph discoverability).

---

## Core Hubs

The following pages are the primary hubs of the link graph. Every expansion page must connect to at least one of these.

```
/                         — Primary Gateway
/framework/               — Central Analytical Hub
/methodology/             — Trust and Evaluation Hub
/sources/                 — Source Registry Hub
/tools/                   — Decision Tools Hub
/feasibility-and-constraints/  — Credibility Hub
/strategic-importance/    — Strategic Context Hub
/global-programs/         — Institutional Registry Hub
/glossary/                — Terminology Hub
/articles/                — Analysis Gateway Hub
```

---

## Universal Link Requirements

Every published page must satisfy all four requirements:

| Requirement | Rule |
|---|---|
| **Parent Hub** | Must link to exactly one parent hub from the core hub list |
| **Related Links** | Must link to at least two related pages |
| **Trust Link** | Must link to `/methodology/` or `/sources/` |
| **Next-Step Link** | Must link to one page that deepens or continues the reader's path |

---

## Link Rules by Page Type

### Glossary Term

```
Parent Hub: /glossary/
Required Links:
  - /glossary/ (parent)
  - One related glossary term
  - One concept reference page (e.g. /framework/ or /technology-stack/)
Trust Link: /sources/ or /methodology/
Next-Step Link: one question page or deeper reference page
```

### Question Answer

```
Parent Hub: /what-is-space-based-solar-power/ or relevant topic hub
Required Links:
  - Parent hub
  - One glossary term (if applicable)
  - One reference page (methodology or sources)
Trust Link: /methodology/ or /sources/
Next-Step Link: a deeper reference or tool page
```

### Comparison Page

```
Parent Hub: /feasibility-and-constraints/ or /framework/
Required Links:
  - Both subject reference pages
  - /methodology/ (claim discipline)
Trust Link: /sources/
Next-Step Link: /tools/ or relevant constraint page
```

### Country Profile

```
Parent Hub: /global-programs/
Required Links:
  - /global-programs/
  - /strategic-importance/
  - /sources/
Trust Link: /methodology/
Next-Step Link: relevant program profile or /feasibility-and-constraints/
```

### Program Profile

```
Parent Hub: /global-programs/
Required Links:
  - /global-programs/
  - /technology-stack/ (if technical program)
  - /sources/
Trust Link: /methodology/
Next-Step Link: /feasibility-and-constraints/ or /strategic-importance/
```

### Use Case Profile

```
Parent Hub: /strategic-importance/ or /tools/
Required Links:
  - Parent hub
  - /feasibility-and-constraints/
  - /sources/
Trust Link: /methodology/
Next-Step Link: relevant constraint page or program profile
```

### Constraint Page

```
Parent Hub: /feasibility-and-constraints/
Required Links:
  - /feasibility-and-constraints/
  - /technology-stack/ or /framework/
  - /sources/
Trust Link: /methodology/
Next-Step Link: /tools/ or related constraint page
```

### Source Brief

```
Parent Hub: /sources/
Required Links:
  - /sources/
  - One or more pages that cite the source
Trust Link: /methodology/
Next-Step Link: one related source brief or reference page
```

### Audience Guide

```
Parent Hub: / (home)
Required Links:
  - /methodology/ or /sources/
  - /tools/
  - Two or more recommended reference pages
Trust Link: /methodology/
Next-Step Link: /tools/ or most relevant reference page
```

---

## Hub Outbound Link Budget

Hubs must not exceed their maximum outbound links to remain navigable.

| Hub | Max Outbound Links |
|---|---|
| `/` | 20 |
| `/framework/` | 40 |
| `/methodology/` | 30 |
| `/sources/` | 50 |
| `/feasibility-and-constraints/` | 50 |
| `/global-programs/` | 100 |
| `/tools/` | 30 |
| `/glossary/` | 200 |
| `/articles/` | 100 |

When a hub exceeds its budget, the system must create a sub-hub or cluster index page before adding more links.

---

## Orphan Prevention

An orphan page is any page in `public/` that has zero inbound links from other published pages.

Orphan pages:

- cannot be discovered by crawlers following links;
- are treated by Google as lower-confidence content;
- weaken the link graph's authority transfer.

`validate_internal_link_graph.py` scans all generated pages, builds an inbound-link index, and fails the build if any page has zero inbound links from other approved pages.

The sitemap alone is not a substitute for inbound links.

---

## Link Text Rules

| Rule | Requirement |
|---|---|
| No generic anchor text | Never use "click here", "read more", "link", "here" |
| Descriptive anchors | Anchor text must describe the destination page topic |
| No keyword stuffing | Do not repeat exact-match keywords in every anchor |
| Natural variation | Use natural phrasing and synonyms across link text |

---

## Cross-Language Link Rules

- English pages must not link to untranslated localized editions.
- Localized pages must link to their English source page.
- `hreflang` tags may only reference published, validated, approved language editions.
- See `validate_hreflang.py` for enforcement logic.

---

## Internal Link Graph File

The full graph is defined in:

```
main/data/internal_link_graph.json
```

The build system reads this file to inject contextual links into generated pages. Manual link insertion in page content is allowed only for core reference pages; all generated pages must derive their links from the graph file.
