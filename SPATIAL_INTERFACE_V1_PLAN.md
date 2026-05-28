# Spatial Interface v1 — Implementation Plan

## Purpose

This document defines the first real implementation of the Sovereign Spatial Interface for Space-Based-Solar-Power.com. It specifies the required structural zones, HTML components, CSS classes, behavioral constraints, and quality limits for the interface architecture that replaces the current baseline template system.

This plan governs the `feat(ui)` work in Sprint 2. All implementation must follow `INTERFACE_THESIS.md`. No element may be added that is not specified here or that violates the UX principles in the thesis.

---

## 1. Mission Control Header

### Purpose

The header establishes the institutional identity of the asset and signals that the user has entered a governed reference system. It is not a product nav bar, marketing header, or decorative strip.

### Required elements

- **Home link** — text logo `Space-Based Solar Power`, links to `/`.
- **Mission status indicator** — a small status dot with the label `Reference Active`. This indicates the asset is a live, maintained reference system. It uses a real CSS dot, not an icon or external asset.
- The status indicator must be semantically neutral — it is a label, not a fake operational readout.

### CSS classes

- `.site-header` — sticky header, dark surface, bottom border.
- `.site-nav` — max-width constrained flex row.
- `.home-link` — uppercase condensed text, no underline.
- `.mission-status` — right-aligned flex row with dot and label.
- `.mission-status-dot` — 6px circle, accent color.

### Constraints

- No dropdown navigation in v1.
- No external icon libraries.
- No JavaScript required for header behavior.
- Header must remain fully functional without CSS (degrades gracefully to plain text links).

---

## 2. Telemetry Sidebar / Mobile Telemetry Stack

### Purpose

The telemetry panel displays the seven core system layers defined in `INTERFACE_THESIS.md` as structured status cards. It provides the user with an immediate structural map of the SBSP infrastructure chain.

This is not fake telemetry. Every card represents a real layer in the infrastructure chain with an honest phase indicator based on the documented state of the technology.

### Required elements (7 cards, one per layer)

Each card contains:
- **Label** — the layer name (e.g. `Orbital Core`).
- **Value** — the layer description (e.g. `Solar Collection Array`).
- **Phase** — the current research/development phase (e.g. `Research Phase`).

Layer definitions (canonical values, must not be modified without a DECISION_LOG entry):

| Layer | Value | Phase |
|---|---|---|
| Orbital Core | Solar Collection Array | Research Phase |
| Power Beaming Vector | Microwave / Laser Transmission | Demonstration Phase |
| Rectenna / Terrestrial Reception | Ground Reception Infrastructure | Concept Phase |
| Grid Resilience | National Energy Infrastructure | Strategic Study |
| AI Energy Demand | High-Density Compute Power | Emerging Pressure |
| Defense / Disaster Resilience | Strategic Power Continuity | Strategic Framing |
| Lunar & Space-Industrial | Off-Earth Infrastructure | Concept Phase |

### Layout behavior

- **Desktop**: 7-column grid (or auto-fit minimum 180px columns), arranged horizontally below the hero.
- **Mobile**: 2-column grid, stacked vertically.
- No horizontal scroll.

### CSS classes

- `.telemetry-panel` — grid container, 1px gap background simulating panel borders.
- `.telemetry-card` — individual card, dark surface, padded.
- `.telemetry-card-label` — uppercase small label.
- `.telemetry-card-value` — readable value text.
- `.telemetry-card-phase` — accent-colored phase indicator.

### Constraints

- Phase labels must reflect documented research/program state, not marketing claims.
- No numerical values in telemetry cards.
- No blinking, pulsing, or animated indicators in v1.
- Reduced motion: no transition on any card element.
- Accessible: panel has `aria-label="Infrastructure system layers"`.

---

## 3. Orbital Atlas Hero

### Purpose

The hero introduces the governing thesis of the asset. It is not a marketing tagline or decorative banner. It is the conceptual entry point of the reference system.

### Required elements

- **Eyebrow** — small uppercase label: `Orbital Energy Reference Layer`.
- **Hero title** — the primary conceptual statement: `Moving energy sovereignty above the atmosphere.`
- **Subtitle** — one sentence explaining what the asset covers.
- **Thesis blockquote** — the full governing thesis of the asset, rendered as a left-border blockquote.

### CSS classes

- `.orbital-atlas-hero` — hero container, bottom border, vertical padding.
- `.hero-eyebrow` — uppercase accent-colored label.
- `.hero-title` — large heading-weight statement.
- `.hero-subtitle` — muted supporting sentence.
- `.hero-thesis` — dark surface blockquote with left accent border.

### Constraints

- Hero title must be a `<p>` tag (not an additional `<h1>`) since the page `<h1>` is the page title.
- No background image, gradient overlay, or decorative graphic in v1.
- No JavaScript required.
- No external assets.

---

## 4. Power-Beaming Visual Metaphor

### Purpose

The power-beaming metaphor communicates the directional nature of the SBSP value chain: energy flows from orbit, through transmission, to Earth. This is expressed through layout geometry and typographic direction, not through decorative graphics.

### v1 Implementation

In v1, the power-beaming metaphor is expressed through the telemetry panel layout and its reading order: the layers are presented in system-chain order (Orbital Core at top/left, terrestrial layers progressing downward/rightward). No decorative beam graphic is added in v1.

### Future implementation (v2+)

In a future version, the power-beaming metaphor may be expressed through:
- A CSS-only directional connector element between the orbital layer card and the terrestrial layer cards.
- An SVG inline diagram (no external file dependency) showing the system chain.
- A WebGL layer (after full static baseline approval) expressing beam geometry.

### Constraints

- No decorative beam graphic in v1.
- No external SVG files.
- No JavaScript-dependent animation in v1.

---

## 5. Rectenna / Grid Infrastructure Section

### Purpose

The rectenna and grid infrastructure section grounds the orbital system in its terrestrial consequence. It connects the transmission layer to real infrastructure concerns: reception sites, grid integration, land use, and strategic resilience.

### v1 Implementation

In v1, this section is represented through the telemetry panel (Layer 3: Rectenna / Terrestrial Reception and Layer 4: Grid Resilience) and through the reference atlas links to `/feasibility-and-constraints/` and `/framework/`.

The `feasibility-and-constraints` page carries the full constraint analysis, including rectenna and grid integration constraints.

### Future implementation (v2+)

A dedicated infrastructure section below the telemetry panel may express:
- Rectenna site geometry (CSS grid, no external images).
- Grid integration constraint summary.
- Link to the full Orbital Energy Constraint Matrix.

---

## 6. Constraint Matrix Preview

### Purpose

The constraint matrix preview makes the barriers to SBSP maturity immediately visible to any user who reaches the home page. It communicates institutional seriousness — this asset does not ignore the hard problems.

### Required elements

A structured preview table showing the five primary active constraints:

| Constraint | Status |
|---|---|
| Launch Economics | Active Constraint |
| Orbital Assembly at Scale | Active Constraint |
| Wireless Transmission Performance | Active Constraint |
| Rectenna Deployment Scale | Active Constraint |
| Safety and Regulatory Acceptance | Active Constraint |

A header row showing: `Orbital Energy Constraint Matrix — Preview` with a link to the full analysis page (`/feasibility-and-constraints/`).

### CSS classes

- `.constraint-matrix-preview` — bordered container.
- `.constraint-matrix-header` — dark surface header row with title and link.
- `.constraint-matrix-title` — uppercase label.
- `.constraint-matrix-link` — accent link to full analysis.
- `.constraint-row` — flex row with name and status badge.
- `.constraint-name` — readable constraint label.
- `.constraint-status` — amber/boundary-colored badge.

### Constraints

- No numerical values in v1 constraint preview.
- Constraint labels must match the governed constraint taxonomy.
- Link to full analysis must resolve to an approved_for_launch path.
- No JavaScript required.

---

## 7. Reference Atlas Navigation

### Purpose

The reference atlas navigation provides structured entry points to all major sections of the reference system. It is not a standard site nav or link list. It is a spatial grid of reference cards, each positioned as a specific layer or perspective in the orbital energy infrastructure system.

### Required elements

A grid of reference cards, one per approved core reference section. Each card contains:
- **Category label** — the layer or role of the section (e.g. `Infrastructure Map`, `Constraint Analysis`).
- **Title** — the section name (e.g. `Framework`, `Feasibility and Constraints`).
- **Short description** — one sentence explaining what the section provides.

### CSS classes

- `.ref-atlas-nav` — section container with label.
- `.ref-atlas-nav-label` — uppercase section header.
- `.ref-atlas-grid` — CSS grid of cards.
- `.ref-atlas-card` — individual card, block link, hover state.
- `.ref-atlas-card-label` — small uppercase category label.
- `.ref-atlas-card-title` — card title text.
- `.ref-atlas-card-desc` — muted description text.

### Constraints

- Cards may only link to `approved_for_launch` paths.
- No card may link to a page not in the approved routes set.
- All links must be standard `<a>` elements, not JavaScript-driven navigation.
- Grid must work on mobile (single column) without horizontal scroll.

---

## 8. Trust / Source Layer

### Purpose

The source/trust layer communicates the asset's institutional posture on claims, source discipline, and boundary marking. It appears on the home page to establish trust immediately. It is not a disclaimer; it is a proof of methodological seriousness.

### Required elements

- **Label** — `Source & Methodology Posture`.
- **Statement** — two to three sentences describing the source discipline policy.
- **Links** — links to `/methodology/` and `/sources/`.

### CSS classes

- `.source-trust-block` — contained block, dark surface, border.
- `.source-trust-text` — flex text column.
- `.source-trust-label` — uppercase label.
- `.source-trust-desc` — readable statement text.
- `.source-trust-links` — inline link row.

### Constraints

- Must not use a disclaimer tone.
- Must express confidence in the source methodology, not liability hedging.
- Links must resolve to approved_for_launch paths.

---

## 9. Foundation Page Reference Cards

### Purpose

Foundation pages (about, methodology, framework, manifesto, etc.) must not render as plain paragraphs only. Each content section must be wrapped in a structured reference card that communicates information hierarchy and institutional weight.

### Required structure

Each section becomes a reference section card with:
- Header row with section heading.
- Body area with paragraphs.
- Optional section links at the bottom.

### CSS classes

- `.reference-section` — outer card container, border, rounded.
- `.reference-section-header` — dark surface header with h2.
- `.reference-section-body` — padded body area.

---

## 10. Governed Reference Cards (Glossary / Question / Program)

### Purpose

Glossary terms, question pages, and program profiles must render as governed reference cards: structured entries that make the data type, definition/answer, boundary statement, related links, and source/trust links immediately visible.

### Required structure for all reference types

1. **Card type header** — e.g. `Glossary Term`, `Reference Question`, `Program Profile`.
2. **Title / short definition** — prominent and readable.
3. **Full definition / answer / description** — body text.
4. **Boundary statement** — claim or answer boundary, distinctly styled.
5. **Related links** — internal links to related pages.
6. **Source/trust links** — link to `/sources/` and `/methodology/`.

### CSS classes

- `.reference-card` — outer container.
- `.reference-card-type` — type label header.
- `.reference-card-body` — body area.
- `.reference-card-short` — prominent definition/answer.
- `.reference-card-full` — full body text.
- `.reference-card-boundary` — boundary statement area.
- `.reference-card-boundary-label` — label for boundary type.
- `.reference-card-boundary-text` — boundary text.
- `.reference-card-links` — related links row.
- `.reference-card-source-links` — source/trust links footer.
- `.reference-card-source-label` — `Source & methodology` label.

---

## 11. Responsive Behavior

### Mobile (max-width: 640px)

- Telemetry panel: 2-column grid.
- Reference atlas grid: 1-column.
- Source trust block: stacked vertically.
- Constraint matrix: full width.
- Header: reduced padding.
- All text: size-appropriate, no horizontal overflow.

### Tablet (641px – 900px)

- Telemetry panel: 3–4 column grid.
- Reference atlas grid: 2-column.
- All other layouts: same as desktop.

### Desktop (901px+)

- All panels at full max-width.
- Telemetry panel: 7 cards in auto-fit row.
- Reference atlas grid: 3–4 column.

### Constraints

- No horizontal scroll on any viewport.
- No fixed-width elements that break mobile layouts.
- Touch targets minimum 44x44px.

---

## 12. Performance Limits

- No external font loading. System font stack only.
- No external CDN for any asset (CSS, JS, icons, fonts).
- No JavaScript in v1 interface (no `<script>` tags on pages).
- CSS file target: under 20KB uncompressed.
- No base64-encoded images in CSS.
- No CSS `@import` from external sources.
- Total page weight (HTML + CSS): target under 50KB per page.

---

## 13. Accessibility Limits

- All text: minimum WCAG AA contrast (4.5:1 for normal text, 3:1 for large text).
- All interactive elements: keyboard navigable.
- All links: descriptive text (no `click here` or `read more` without context).
- All structural regions: semantic HTML elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<aside>`).
- All navigation elements: `aria-label` on `<nav>` elements.
- Reduced motion: `@media (prefers-reduced-motion: reduce)` disables all transitions and animations.
- No `tabindex` values other than 0 or -1.
- No ARIA attributes that duplicate implicit semantics.

---

## 14. No External CDN Dependency

This is an absolute constraint, not a preference.

Prohibited in v1:

- Google Fonts or any external font CDN.
- Bootstrap, Tailwind, or any external CSS framework CDN.
- Font Awesome, Heroicons, or any external icon CDN.
- Any JavaScript library loaded from a CDN (`cdn.jsdelivr.net`, `unpkg.com`, `cdnjs.cloudflare.com`, etc.).
- Any analytics, measurement, or tracking script (separate from the measurement governance in `README.md`).
- Any image hosted on an external server.

All permitted assets must be:

- Inline in HTML or CSS;
- Hosted in `main/static/` and served from `public/static/`;
- Or expressed as system-native CSS values (system fonts, CSS custom properties, standard web colors).

---

## 15. v1 Scope Boundary

The following are explicitly **out of scope for v1** and must not be implemented:

- WebGL or canvas-based rendering.
- JavaScript-dependent interface behavior.
- SVG inline diagrams or illustrations.
- Animated beam or orbit visuals.
- Dark mode toggle (dark is the only mode in v1).
- Language switcher UI (multilingual content not yet published).
- Search functionality.
- Interactive constraint matrix (tools layer, future phase).
- Cookie consent UI.
- Social share buttons or external embeds.

---

## 16. Quality Gate Alignment

All interface changes must pass the full quality gate:

- `validate_seo.py` — title, description, h1, canonical present on all pages.
- `validate_links.py` — all internal links resolve to `approved_for_launch` paths.
- `validate_sitemap.py` — sitemap unchanged (no new pages added by interface work).
- `validate_schema.py` — no data file changes required for template upgrades.
- `validate_content.py` — no content file changes required for template upgrades.

Interface work touches only: `main/scripts/build.py`, `main/static/css/main.css`, and `public/` generated output.
