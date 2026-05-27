# Sitemap Policy

## Purpose

This document defines the sitemap architecture, generation rules, and validation requirements for Space-Based-Solar-Power.com.

A sitemap is a signal to Google, not a guarantee of indexing. Google does not promise to crawl or index every URL in a sitemap. However, a well-structured sitemap, combined with strong internal linking, gives Google the best possible input for efficient crawling and correct authority understanding.

This policy exists to prevent:

- draft or placeholder pages entering the sitemap;
- blocked routes appearing in the sitemap;
- sitemap files exceeding Google's 50,000-URL or 50MB limit;
- sitemap index referencing non-existent sitemap files;
- sitemap URLs with canonical mismatches;
- sitemaps that are not submitted to Google Search Console.

---

## Sitemap Architecture

At launch (13 core pages), a single `sitemap.xml` is sufficient.

As the asset grows, the system generates a `sitemap_index.xml` that references individual sitemap files by content type.

### Phase 1: Single Sitemap (up to 500 URLs)

```
public/
  sitemap.xml     (all approved pages)
  robots.txt      (references sitemap.xml)
```

### Phase 2: Sitemap Index (500–50,000 URLs)

```
public/
  sitemap_index.xml
  sitemaps/
    sitemap-core.xml
    sitemap-glossary-001.xml
    sitemap-questions-001.xml
    sitemap-programs-001.xml
    sitemap-countries-001.xml
    sitemap-articles-001.xml
    sitemap-usecases-001.xml
    sitemap-comparisons-001.xml
    sitemap-sources-001.xml
  robots.txt      (references sitemap_index.xml)
```

### Phase 3: Multi-Batch Sitemap Index (50,000+ URLs)

When any individual sitemap file approaches 10,000 URLs, a new batch file is created:

```
sitemaps/sitemap-glossary-001.xml   (entries 1–10,000)
sitemaps/sitemap-glossary-002.xml   (entries 10,001–20,000)
```

The sitemap index is regenerated automatically to reference all batch files.

---

## URL Eligibility Rules

A URL may enter a sitemap only if ALL of the following are true:

1. The page exists in `public/` as a generated HTML file.
2. The page has `sitemap: true` in `pages.json` or its data source.
3. The page has an approved publication status (`approved_for_launch` or equivalent).
4. The page has a valid canonical URL matching its own path.
5. The page is not marked `robots: noindex`.
6. The page has passed all validators in the quality gate.
7. The page is not a `blocked` or `future` or `draft` page.
8. The page has at least one inbound internal link from another approved page.

---

## Sitemap XML Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://space-based-solar-power.com/</loc>
    <lastmod>2026-05-27</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

**Rules:**
- `<loc>` must use the canonical HTTPS domain
- `<lastmod>` must use ISO 8601 format (YYYY-MM-DD)
- `<changefreq>` must match the value in `pages.json`
- `<priority>` must match the value in `pages.json`

---

## Sitemap Index XML Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://space-based-solar-power.com/sitemaps/sitemap-core.xml</loc>
    <lastmod>2026-05-27</lastmod>
  </sitemap>
</sitemapindex>
```

---

## robots.txt Format

### Phase 1 (single sitemap)

```
User-agent: *
Allow: /
Disallow: /draft/
Disallow: /staging/
Sitemap: https://space-based-solar-power.com/sitemap.xml
```

### Phase 2+ (sitemap index)

```
User-agent: *
Allow: /
Disallow: /draft/
Disallow: /staging/
Sitemap: https://space-based-solar-power.com/sitemap_index.xml
```

---

## Language Edition Sitemap Rules

- Localized pages that are published and approved may appear in language-specific sitemap files.
- Pages with `status: planned` or `status: future` must not appear in any sitemap.
- The `hreflang` attribute in the sitemap entry is optional but must be correct if present.

---

## Google Search Console Submission

After every significant expansion (100+ new URLs), the sitemap must be re-submitted to Google Search Console.

The submission URL is:

```
https://search.google.com/search-console
```

This is a manual step, not automated by the build system.

---

## Validation Responsibility

`validate_sitemap.py` enforces all rules above automatically.

No sitemap file may be committed to the repository without passing this validator.
