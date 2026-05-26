# Content Source Model: Space-Based-Solar-Power.com

## 1. Purpose

This document defines the controlled content source model for Space-Based-Solar-Power.com.

The asset must not be built from loose HTML pages, improvised copy, generic blog posts, or unstructured content blocks.

Every public page must be generated from a controlled content source file that defines:

- route;
- title;
- metadata;
- strategic role;
- audience;
- content sections;
- internal links;
- SEO cluster;
- source boundaries;
- claim boundaries;
- publication status.

The content source model exists to make the asset scalable, auditable, multilingual, SEO-controlled, and quality-gate ready.

---

## 2. Governing Rule

Every page source file must answer:

```text
Why does this page exist?
Who is it for?
What strategic role does it serve?
What does it link to?
What claims does it make?
What sources or claim boundaries support those claims?
How does it strengthen the asset?
```

No public page may be created without this structure.

---

## 3. Required Page Fields

Each page content file must contain the following fields:

```json
{
  "id": "",
  "route": "",
  "language": "en",
  "pageType": "",
  "status": "",
  "title": "",
  "metaDescription": "",
  "h1": "",
  "strategicRole": "",
  "primaryAudience": [],
  "seoCluster": [],
  "hero": {},
  "sections": [],
  "internalLinks": [],
  "sourceNotes": [],
  "claimBoundary": "",
  "qualityStatus": {}
}
```

---

## 4. Field Definitions

### `id`

Stable internal identifier matching `main/data/pages.json`.

### `route`

Canonical route for the page.

Example:

```text
/framework/
```

### `language`

Primary language of the content source.

Initial allowed value:

```text
en
```

Localized pages require separate reviewed content sources.

### `pageType`

The page type from `pages.json`.

Examples:

```text
sovereign_gateway
trust_page
methodology_page
reference_hub
conceptual_anchor
source_registry_page
tools_gateway
analysis_gateway
foundational_reference
technical_reference
credibility_hub
strategic_reference
institutional_registry_hub
```

### `status`

Allowed values:

```text
draft
review
approved_for_launch
blocked
```

A page may not enter production unless its status is `approved_for_launch` and quality validation passes.

### `strategicRole`

Defines why the page exists inside the sovereign asset system.

### `primaryAudience`

Defines the audiences served by the page.

Approved examples:

```text
researchers
journalists
investors
governments
companies
engineers
analysts
strategic buyers
general serious readers
```

### `seoCluster`

Defines the search clusters served by the page.

No page may target random keywords outside the approved content strategy.

### `hero`

The hero object must include:

```json
{
  "eyebrow": "",
  "title": "",
  "subtitle": "",
  "thesis": ""
}
```

### `sections`

Each section must include:

```json
{
  "id": "",
  "heading": "",
  "body": [],
  "links": [],
  "sourceRefs": []
}
```

The `body` field should be an array of paragraphs.

### `internalLinks`

Every page must define required internal links.

Each link should include:

```json
{
  "label": "",
  "path": "",
  "reason": ""
}
```

### `sourceNotes`

Source notes must use source IDs from `main/data/sources.json` where available.

Example:

```json
{
  "sourceId": "nasa-otps-sbsp-2024",
  "usage": "Used for feasibility and constraint framing."
}
```

### `claimBoundary`

Defines how claims on the page must be interpreted.

Example:

```text
This page provides conceptual and strategic framing. It does not claim that SBSP is commercially mature or technically resolved.
```

### `qualityStatus`

The quality status must include:

```json
{
  "metadataComplete": true,
  "internalLinksDefined": true,
  "sourceBoundaryDefined": true,
  "placeholderFree": true,
  "readyForTemplate": true
}
```

---

## 5. Source Discipline

Every page must distinguish between:

- conceptual framing;
- source-verified facts;
- institutional summaries;
- technical explanations;
- strategic interpretation;
- company claims;
- unresolved scenarios;
- speculative future pathways.

Speculation is allowed only when clearly labeled.

Speculation must never be presented as established fact.

---

## 6. Internal Link Rule

Every page must link to:

1. one parent hub;
2. at least two related pages;
3. one trust page such as `/methodology/` or `/sources/`;
4. one next-step route such as `/tools/`, `/framework/`, or a relevant reference page.

No page may be an isolated content island.

---

## 7. Launch v1 Content Sources

The first content source files required for Sovereign Reference Launch v1 are:

```text
main/content/pages/home.json
main/content/pages/about.json
main/content/pages/methodology.json
main/content/pages/framework.json
main/content/pages/manifesto.json
main/content/pages/sources.json
main/content/pages/tools.json
main/content/pages/articles.json
main/content/pages/what-is-space-based-solar-power.json
main/content/pages/technology-stack.json
main/content/pages/feasibility-and-constraints.json
main/content/pages/strategic-importance.json
main/content/pages/global-programs.json
```

---

## 8. Anti-Placeholder Rule

The following are prohibited in content source files:

```text
Lorem ipsum
Coming soon
Under construction
TODO
Placeholder
Dummy text
Fake article
Fake author
Fake date
Fake live tool
Unsupported statistic
Unlabeled scenario number
```

---

## 9. Multilingual Rule

Localized content must not be raw machine translation.

Each localized file must preserve:

- technical accuracy;
- source boundaries;
- institutional tone;
- localized strategic emphasis;
- metadata quality;
- hreflang integrity;
- RTL safety where applicable.

No localized page may enter production without review.

---

## 10. Conclusion

The content source model is the bridge between governance and publication.

It ensures that Space-Based-Solar-Power.com can scale into a large reference asset without becoming random, thin, unsourced, or technically fragile.
