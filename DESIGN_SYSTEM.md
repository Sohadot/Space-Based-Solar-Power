# Design System: Space-Based-Solar-Power.com

## 1. Design System Purpose
This design system governs the visual, spatial, typographic, motion, accessibility, and multilingual behavior of Space-Based-Solar-Power.com. 

The design system must not create a generic technology interface. It must support a thesis-driven sovereign interface that embodies orbital energy infrastructure, energy sovereignty, wireless power transmission, and future space-industrial systems.

## 2. Design Principle
The governing design principle is:
> The interface must not decorate the asset. The interface must embody the asset’s thesis.

Every visual decision must connect to at least one of the following core dimensions:
* orbital energy collection;
* power beaming;
* terrestrial reception;
* grid resilience;
* AI energy demand;
* defense and disaster-response infrastructure;
* lunar and space-industrial extension;
* multilingual global authority;
* institutional trust.

## 3. Approved Visual Character
The asset visual persona is rigorously restricted to the following attributes:
* **sovereign:** commands geopolitical and structural authority;
* **spatial:** natively oriented toward orbital mechanics and deep cosmic geography;
* **embodied:** visual vectors map directly to physical infrastructure reality;
* **infrastructural:** treats pages as operational tools rather than marketing surfaces;
* **precise:** rejects approximation; layout lines match technical specifications;
* **cinematic with purpose:** motion is deployed strictly to map spatial scale;
* **institutional:** addresses sovereigns, capital allocators, and researchers;
* **deep-tech:** completely untethered from consumer-focused web aesthetics;
* **alive without chaos:** retains structural movement without dynamic distraction.

## 4. Rejected Visual Character
The project explicitly prohibits:
* generic dark SaaS product layouts;
* decorative sci-fi dashboards or cyberpunk telemetry;
* gaming aesthetics, over-saturated hues, or fictional planetary visuals;
* childish or low-fidelity space illustrations;
* random, non-functional neon grids;
* crypto-style tokenomics interface language;
* low-trust, unverified stock photography;
* excessive or non-functional glassmorphism/blur overlays;
* visual transitions that do not isolate or explain structural data.

## 5. Color System
The color system expresses orbital energy capture, deep space void isolation, precision infrastructure, and directed electromagnetic power transfer.

### Approved Core Palette Matrix
```css
:root {
  /* The Spatial Grid Base */
  --space-void: #06070d;         /* The baseline cosmic matrix; eliminates edge bleeding */
  --space-depth: #0a0d16;        /* Subtle contrast depth for layout structures */
  --infra-dark: #0d111c;         /* Structural panels, container backgrounds, and control hulls */

  /* Institutional Typography Layer */
  --text-primary: #f8fafc;       /* High-contrast analytical assertions and headers */
  --text-secondary: #cbd5e1;     /* Technical bodies and primary summaries */
  --text-muted: #94a3b8;         /* Citation footprints, sources, and metadata logs */

  /* The Orbital Solar Vector */
  --orbital-gold: #f4d068;       /* Photovoltaic capture; non-saturated technical gold */
  --orbital-gold-soft: #d9b95d;  /* Shaded orbital geometry surfaces */

  /* The Transmission Vector */
  --beaming-cyan: #00d9ff;       /* Wireless power beaming; electromagnetic beam telemetry */
  --beaming-cyan-soft: #7ddff2;  /* Coherent atmospheric penetration wave trace */

  /* Operational Infrastructure Signals */
  --grid-blue: #4f8cff;          /* Terrestrial utility grid integration signals */
  --signal-green: #9fffc2;       /* Active link validation, live nodes, and audited sources */

  /* Borders and Containers */
  --line-subtle: rgba(255, 255, 255, 0.08);
  --panel-dark: rgba(13, 17, 28, 0.78);
}

```
 * **Rule of Noise:** The color palette must not become visually noisy.
 * **Functional Identity:** Gold represents orbital solar collection. Cyan represents wireless transmission and signal structure. Deep blue/black represents controlled space infrastructure. Muted text tones preserve institutional seriousness.

## 6. Typography
Typography must be clear, institutional, and technically serious. The system utilizes stable platform-native font stacks before introducing external network fonts.

### Base Content Font Stack (High-Legibility Reading Surfaces)
```css
font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;

```
### Technical/Data Font Stack (Matrices, Tools, and Citations)
```css
font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;

```
 * **Constraint:** External web-font injection requires a documented performance, security policy, and licensing decision under PROJECT_DOCTRINE.md.

## 7. Layout System
The structural mechanics must support large conceptual sections, high-prestige text layouts, spatial canvas backgrounds, multilingual expansion, Arabic RTL processing, tool panels, and extensive reference tables.
To enforce native bi-directional parity, the system mandates the use of CSS Logical Properties:
```css
/* Core Layout Blueprint Rules */
padding-inline: var(--spacing-unit);
margin-inline: auto;
border-inline-start: 2px solid var(--beaming-cyan);
border-inline-end: none;
text-align: start;
inset-inline: 0;
inline-size: 100%;
block-size: auto;

```
 * **Constraint:** Hard-coded spatial assumptions (left, right) are strictly prohibited in global layouts.

## 8. RTL and Multilingual Support
The asset is built to serve English, Arabic, Chinese, Japanese, French, German, and Spanish. No component may assume English text density.

 * **Arabic Layout Execution:**
   ```html
   <html lang="ar" dir="rtl">
   
   ```
 * **LTR Bloc Layout Execution:**
   ```html
   <html lang="en" dir="ltr">
   
   ```
 * **Structural Integrity Guardrails:** No navigation element may break wrap bounds when translated. The language switcher is structurally barred from generating routes to draft or unpublished variants as defined in pages.json.

## 9. Spatial Interface Rules
WebGL, Three.js, canvas rendering, or spatial motion operate strictly as **progressive enhancements**.
 * The static HTML page must remain 100% readable, complete, and functional if WebGL fails, is blocked by corporate firewalls, or is disabled by user environment constraints.
 * Spatial elements must natively honor browser reduced-motion media queries (prefers-reduced-motion). They must not obscure text, distort interactive tools, or dominate mobile viewpoints.

## 10. Motion System
Motion is explicitly treated as a functional vector to communicate energy-logistical scale.

### Approved Kinetics

 * unaccelerated, slow orbital drift mimicking geosynchronous objects;
 * controlled, synchronized beam pulses tracking atmospheric pathing;
 * grid-line micro-activations upon calculations or value shifts;
 * heavy-inertia cinematic camera movements tied directly to active viewport scroll states.

### Prohibited Kinetics

 * random particle fields, meteor rains, or non-functional star-travel matrices;
 * constant aggressive looping animations that exhaust host GPU resources;
 * distracting parallax scripts that decouple text layers from reading planes;
 * gaming-style free-fly camera systems that disorient the enterprise user.

## 11. Accessibility Requirements
No visual effect may be allowed to degrade accessibility benchmarks. The production interface must guarantee:
 * validated semantic HTML element selection;
 * WCAG AAA readable contrast thresholds across all technical text layers;
 * complete keyboard navigation support with high-visibility focus states;
 * explicit text-first comprehension layers that do not rely on audio-visual cues.

## 12. Performance Requirements
Initial production builds must prioritize a highly optimized, ultra-lightweight static shell.
Future WebGL modules require isolated local bundling (zero external CDN delivery), rigid compliance with the project's Content Security Policy (SECURITY_POLICY.md), performance testing on restricted mobile bandwidth, and full fallback layer testing before merging into the production branch.

## 13. Component Classes
The architecture is modular, enforcing consistency across all language variants via specific component classes:
 * sovereign-header: Global metadata branding bar and language selectors.
 * spatial-hero: The canvas docking surface containing the core thesis.
 * thesis-panel: Typographic containment blocks for analytical copy.
 * constraint-matrix: Grid boards housing simulator variable sliders.
 * reference-card & source-list: Sourced academic and institutional reference layers.
 * footer-governance-strip: The ultimate layer hosting decision log codes and copyright.

## 14. Trust and Buyer Perception

The final structural output must immediately project to institutional auditors that the asset is:

1. **Governed:** Built through institutional methodology, documented decisions, and controlled development standards.
2. **Source-Disciplined:** Transparent, factual, claim-boundary disciplined, and supported by verifiable references.
3. **Acquisition-Ready:** Highly engineered, scalable, multilingual, and difficult to replicate without substantial conceptual, technical, editorial, and interface-design effort.

The design must never make the asset feel like a disposable landing page, a generic technology template, or a speculative visual experiment.
