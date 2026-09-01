# Botesdale Dental — Design System

Version 1.0 · Living document
Reference implementation: **`pages/style-guide.html`** (open it in a browser — every component below is rendered there)

---

## 1. Principles

The reference for this system is precision-engineering brand design — Porsche in particular. That translates into five working rules:

1. **One rail.** Every piece of text on the site — inside a centred container or inside a full-bleed section — starts or stops on the same vertical line. Media is the only thing allowed to cross it. See §2.3.
2. **Lines, not boxes.** Structure is expressed with 1px hairlines and alignment. Shadows are almost never used; corners are square (`--radius: 0`).
3. **Two grounds.** A warm off-white (`--paper`) and a near-black (`--black`). Every section belongs to one of them. Dark sections are used deliberately, for emphasis, roughly one per screenful of scrolling.
4. **One accent, sparingly.** `--accent` appears in the arc motif, list markers, focus rings and validation. It is never used as a background for large areas.
5. **Editorial rhythm.** Full-bleed media/copy splits, generous vertical space, and a short uppercase micro-label above almost every heading. Copy is left-aligned throughout — including quotes and closing calls to action.
6. **Restrained motion.** 200–480ms, ease-out, and only on hover, reveal and open/close. Everything respects `prefers-reduced-motion`.

### The arc

The practice's signature motif is a shallow arc — a smile. It appears in two places:

* **`.arc`** — an inline SVG stroke that draws itself in under links, nav items and tabs on hover.
* **`#smileClip`** — an SVG `clipPath` that gives button hover-fills a curved leading edge.

Both are defined once per page (`<svg class="svg-defs">`) and referenced everywhere. If you remove the `svg-defs` block, buttons lose their curved fill.

---

## 2. Tokens

All tokens live in **`css/base.css`** under `:root`. Nothing below that block hard-codes a colour or a size. Change a token and it propagates site-wide.

### 2.1 Colour

| Token | Value | Use |
|---|---|---|
| `--black` | `#0E1116` | Ink. Headings, dark sections, solid buttons |
| `--black-800` | `#1A1F26` | Secondary dark surface |
| `--paper` | `#F7F6F3` | The page ground |
| `--paper-2` | `#FFFFFF` | Pure white, used sparingly for lift |
| `--paper-3` | `#EFEDE8` | Alternating section band |
| `--placeholder` | `#E5E3DC` | Image placeholder ground |
| `--placeholder-2` | `#DCDAD2` | Image placeholder on a tinted band |
| `--ink-soft` | `#5B615F` | Body copy on paper |
| `--ink-mute` | `#8A8F8C` | Meta, captions, placeholders |
| `--line` | `#D9D7D0` | Hairline on paper |
| `--line-dark` | `rgba(247,246,243,.18)` | Hairline on black |
| `--paper-soft` | `rgba(247,246,243,.70)` | Body copy on black |
| `--paper-mute` | `rgba(247,246,243,.45)` | Micro-labels on black |
| `--accent` | `#17A6DE` | Arc motif, markers, focus, validation |
| `--accent-600` / `--accent-700` | `#1189BB` / `#0B6E97` | Hover / small text on light |
| `--ok` `--warn` `--error` | `#1D7A57` `#8A5A00` `#A93226` | Notices and form validation |

> **Note on the brand blue.** The written brief specifies `#009ee3`. The approved design system uses `#17A6DE`, which sits better against the warm paper ground. To switch, change `--accent` (and optionally `--accent-600/700`) in `css/base.css` — nothing else needs touching.

**Dark grounds** for the hero and page heads: `--grad-hero`, plus `--grad-cool`, `--grad-warm`, `--grad-slate` if a gradient panel is ever needed. Media panels awaiting photography use `--placeholder` (see §4.4).

**Contrast.** `--ink-soft` on `--paper` is 6.4:1; `--paper-soft` on `--black` is 9.5:1. Both clear WCAG AA for body text. `--accent` is only used for large text, borders and iconography — never for small body copy on paper.

### 2.2 Typography

Two families, loaded from Google Fonts with a full system fallback stack:

* **Space Grotesk** (`--font-head`) — 400/500/600/700. Headings, micro-labels, numerals, buttons.
* **Inter** (`--font-body`) — 400/500/600. Body copy, forms, captions.

Every size is fluid, interpolating between a mobile and a desktop value with `clamp()`:

| Token | Range | Class / element |
|---|---|---|
| `--fs-hero` | 30 → 68px | `.display` |
| `--fs-h1` | 28 → 52px | `h1` |
| `--fs-h2` | 24 → 34px | `h2` |
| `--fs-h3` | 20 → 24px | `h3`, `.statement-text` |
| `--fs-h4` | 17px | `h4` |
| `--fs-lead` | 15 → 17px | `.lead`, `.prose p` |
| `--fs-body` | 15px | `body` |
| `--fs-sm` / `--fs-xs` | 14 / 13px | secondary copy, meta |
| `--fs-label` | 11px, `.16em` tracking | `.label` |

Tracking tightens as size increases (`--ls-tight: -.02em` on `h1` and `.display`). Line height is `1.08` for display, `1.2` for headings, `1.7` for body.

**Measure.** Long-form copy is capped at `--measure` (640px) via `.prose` or `.u-measure`.

### 2.3 The content rail and the bleed grid

`--wrap` (1200px) is the maximum width of any line of text on the site. A centred `.wrap` puts its content at `(100vw − 1200) / 2 + --pad-inline` from the viewport edge; that line is **the rail**, and everything textual aligns to it.

Full-bleed components — the editorial block and the team row — cannot use `.wrap`, because their media has to run out to the viewport edge. They use a four-column *bleed grid* instead, built from two tokens:

```css
--col-gutter: minmax(var(--pad-inline), 1fr);
--col-half:   minmax(0, calc(var(--wrap) / 2 - var(--pad-inline)));

.ed {
  grid-template-columns: var(--col-gutter) var(--col-half) var(--col-half) var(--col-gutter);
}
.ed__media { grid-column: 1 / 3; }   /* bleeds left, stops at the centre */
.ed__text  { grid-column: 3 / 4; }   /* ends on the rail                 */
.ed--rev .ed__media { grid-column: 3 / 5; }
.ed--rev .ed__text  { grid-column: 2 / 3; }   /* starts on the rail      */
```

Because the gutters are `1fr` and the content columns are capped, the text column lands on exactly the same pixel as a centred `.wrap` at every viewport width — and the measure inside it stays constant as the window grows. No `100vw` arithmetic is involved, so there is no scrollbar-width error.

Two things to know if you extend this:

* Give every child of a bleed grid `grid-row: 1`. Without it, an item whose column starts *before* the auto-placement cursor is pushed onto a second row — which is what silently breaks reversed blocks.
* Below 860px the grid collapses to one column and both children take `padding-inline: var(--rail-x)`, which is simply `--pad-inline` at those widths.

### 2.4 Spacing

A 4px base scale: `--s-1` (4px) through `--s-12` (112px). Section padding uses the fluid `--section-y` / `--section-y-tight` tokens rather than a fixed step, so vertical rhythm scales with the viewport.

Layout tokens: `--wrap` (1200px), `--wrap-wide` (1440px), `--measure` (640px), `--gutter`, `--pad-inline`, `--pad-block`, `--nav-h` (73px).

### 2.5 Motion

`--t-fast` 200ms · `--t` 300ms · `--t-slow` 480ms · `--ease` `cubic-bezier(.4,0,.2,1)` · `--ease-out` `cubic-bezier(.22,.61,.36,1)`.

### 2.6 Z-index ladder

`--z-tabnav` 40 → `--z-dd` 60 → `--z-nav` 80 → `--z-menu` 100 → `--z-top` 120. Never invent a new value; use the ladder.

---

## 3. Breakpoints

The layout is fluid first; these are the only hard breakpoints in the system.

| Width | What changes |
|---|---|
| `≤ 1120px` | Desktop nav hides, burger + full-screen menu appear |
| `≤ 980px` | `.cols-4` → 2 columns |
| `≤ 940px` | `.with-rail` and `.contact-grid` stack |
| `≤ 900px` | `.cols-3` → 2 columns; strip → 2 columns; gallery → 2 columns; footer → 2 columns |
| `≤ 860px` | `.ed` and `.team__row` leave the bleed grid and stack |
| `≤ 620px` | `.cols-*` → 1 column; form grid → 1 column |
| `≤ 540px` | Strip → 1 column |
| `≤ 479px` | Buttons in a `.btn-row` go full width |

---

## 4. Components

Each entry lists the file it lives in, the markup, and the modifiers available. All of them are rendered live in `pages/style-guide.html`.

### 4.1 Button — `components.css`

```html
<a class="btn btn--solid" href="#">
  <span class="btn__fill"></span>
  <span class="btn__label">Book a visit</span>
</a>
```

The `__fill` span sweeps across on hover, clipped by `#smileClip`. The `__label` uses `mix-blend-mode: difference` so it inverts against whatever is behind it — which is why both spans are required.

**Modifiers:** `--solid` (dark), `--outline` (paper), `--light` (for dark grounds), `--sm`, `--block`, `.is-disabled`.
Wrap groups in `.btn-row`.

### 4.2 Arc link — `components.css`

```html
<a class="arc-link" href="#">
  <span>Read more</span>
  <svg class="arc" viewBox="0 0 100 8" preserveAspectRatio="none" aria-hidden="true">
    <path d="M0,1 Q50,7 100,1" pathLength="100"/></svg>
</a>
```

The standard "read more" affordance. `--light` variant for dark sections.

### 4.3 Header & navigation — `layout.css` + `js/nav.js`

Transparent over the hero, then `.is-scrolled` swaps in a translucent paper background once the hero has passed. Desktop dropdowns open on hover and focus (`:focus-within`), so they are keyboard-reachable. Below 1080px the burger opens `.menu`, a full-screen sheet with focus trapping, Escape-to-close and expandable groups.

### 4.4 Image placeholder — `.ph`

Every media area on the site is currently a placeholder rather than a photograph.

```html
<div class="ph" role="img" aria-label="A family smiling together">
  <span class="ph__label">A family smiling together</span>
</div>
```

Flat grey, a hairline inset, and a small uppercase label naming the shot that belongs there. It stretches to fill its parent, so the parent owns the aspect ratio (`.card__media` is 3:2, `.strip__media` is 4:3, `.shot` is 3:2, `.ed__media` fills the row).

**Swapping in real photography:** replace the whole `<div class="ph">` with `<img src="…" alt="…" loading="lazy">`. Nothing else changes — the parents already set `object-fit: cover`.

The hero and page heads are dark panels rather than placeholders; each carries a commented-out `<img class="hero__media">` / `<img class="page-head__media">` showing exactly where the background photograph goes, plus a `.ph-note` marker in the corner. Delete the marker when the image lands.

### 4.5 Hero — `components.css`

```html
<section class="hero">
  <img class="hero__media" src="…" alt="">
  <div class="hero__scrim"></div>
  <div class="hero__inner wrap">…</div>
</section>
```

`margin-top: calc(-1 * var(--nav-h))` pulls it under the transparent header. The scrim is a three-stop gradient that keeps text legible whatever the photograph does.

### 4.6 Page head — `components.css`

The compact hero used on every inner page. Same structure as `.hero`; add `--short` for legal pages. Carries the breadcrumb and, where it is not simply a repeat of the `h1`, a micro-label.

### 4.7 Breadcrumb — `.crumbs`

Uppercase, 11px, with a `/` separator. `--on-paper` variant for use outside a dark page head.

### 4.8 Editorial block — `.ed`

The workhorse: a full-bleed media panel beside a copy column.

```html
<section class="ed" data-reveal>
  <div class="ed__media"><div class="ph">…</div></div>
  <div class="ed__text">
    <span class="label">Philosophy</span>
    <h2>…</h2><p>…</p>
    <a class="arc-link" …>…</a>
  </div>
</section>
```

**Modifiers:** `--rev` (media right, copy starts on the rail), `--warm` (a half-step darker placeholder, for tonal alternation between consecutive blocks).

### 4.9 Strip grid — `.strip`

Hairline-separated tiles, 2–4 up, with a 4:3 media panel that desaturates until hover. Set the count with `.strip__row--2` / `--3`, default 4.

### 4.10 Card — `.card`

A bordered tile for grids that need visible gaps rather than hairline seams. `--dark` variant available.

### 4.11 Statement band — `.statement`

Full-width dark section for a single idea, with optional `.facts` beneath it. Use `.facts--paper` for the same component on a light ground.

### 4.12 Process list — `.p-row`

Numbered hairline rows (`01`, `02`, …). The default way to explain a sequence.

### 4.13 Team row — `.team__row`

Half-width portrait beside a biography. `--rev` alternates the side.

### 4.14 Quote & carousel — `.quote`, `[data-carousel]`

A single quote renders statically; more than one becomes a carousel that auto-advances every 8 seconds and pauses on hover or focus. Dots are generated by `js/ui.js`. Left-aligned on the rail, with the measure capped at `24em` so a long testimonial still reads as a column rather than a wall.

### 4.15 Spec rows — `.specs` / `.spec`

Label/value hairline rows for contact details, opening hours and quick facts. Stacks below 480px.

### 4.16 Plan card & price list — `.plan`, `.price-list`

`.plan--feature` inverts to the dark ground for the headline option. `.price-list__row` handles a description, an optional note and a right-aligned price.

### 4.17 Accordion — `.accordion` + `js/ui.js`

```html
<div class="accordion" data-single>
  <div class="accordion__item">
    <h3><button class="accordion__btn" aria-expanded="false" aria-controls="p1">
      <span>Question</span><span class="accordion__icon"></span></button></h3>
    <div class="accordion__panel" id="p1"><div class="accordion__panel-inner">…</div></div>
  </div>
</div>
```

`data-single` closes siblings on open. Height is animated from the measured `scrollHeight`, and recalculated on resize.

### 4.18 Notice — `.notice`

Left-rule callout. `--ok`, `--warn`, `--error`, `--plain`.

### 4.19 Badge — `.badge`

`--accent`, `--solid`, plus `.pill` for a rounded shape.

### 4.20 Table — `.table` inside `.table-scroll`

Uppercase micro-label header row, hairline separators. The wrapper scrolls horizontally rather than letting the page do so.

### 4.21 Gallery & lightbox — `.gallery`, `.shot`, `#lightbox`

Clinical before/during/after images with a corner tag. Any `[data-lightbox]` figure opens full-screen; Escape or a click closes it.

### 4.22 Rail — `.rail`

Sticky contextual sidebar listing sibling pages, with the current page marked by an accent tick. Used inside `.with-rail`.

### 4.23 Pager — `.pager`

Previous / next split used between case studies.

### 4.24 Forms — `.form`, `.field` + `js/forms.js`

Underlined fields, uppercase micro-labels, and a `.field__error` element that fills in on validation failure.

```html
<div class="field">
  <label for="c-name">Your name <span class="field__req">*</span></label>
  <input id="c-name" name="c-name" type="text" required>
  <span class="field__error" role="alert"></span>
</div>
```

Add `data-validate` and `data-success="<id>"` to the `<form>`. Validation runs on submit, and on blur once a field has been touched. States: `.has-error`, `.is-valid`. Choice controls use `.choice` / `.choice-grid`; long forms are divided with `.form__section-title`.

### 4.25 CTA band — `.cta`

Centred closing block. `--dark` inverts it.

### 4.26 Cookie banner — `.cookie` + `js/ui.js`

Slides up after 900ms unless a choice is already stored in `localStorage` under `bdp-cookie-choice`. Storage access is wrapped in `try/catch` for private-browsing mode.

### 4.27 Back to top — `.to-top`

Appears past 700px of scroll.

### 4.28 Tab nav — `.tabnav` / `.tab` + `js/ui.js`

Sticky in-page jump bar with an `IntersectionObserver` scroll-spy. Sits directly beneath the header (`top: var(--nav-h)`).

### 4.29 Reveal on scroll — `[data-reveal]`

Add the attribute to any element; `js/ui.js` adds `.is-in` when it enters the viewport. `data-reveal-delay="1|2|3"` staggers a group. Disabled entirely under `prefers-reduced-motion`.

---

## 5. Layout utilities

`.wrap` (+ `--wide`, `--text`) · `.grid` with `--min` · `.cols-2/3/4` · `.with-rail` · `.stack` · `.cluster` · `.section` (+ `--tight`, `--paper-3`, `--dark`, `--top-line`) · `.section-head` (+ `--center`) · `.rule` (+ `--dark`, `--tick`).

Text and spacing utilities are prefixed `.u-` (`.u-measure`, `.u-invert`, `.u-mt-6`, `.u-hide-sm`, …). Aspect helpers: `.ar-4-3`, `.ar-3-2`, `.ar-16-9`, `.ar-1-1`, `.ar-3-4`.

---

## 6. Accessibility

* Skip link on every page, first in the tab order.
* One `h1` per page; headings never skip a level.
* Visible focus: `2px solid var(--accent)` with a 3px offset, applied via `:focus-visible`.
* The mobile menu traps focus, closes on Escape and restores focus to the burger.
* Dropdowns open on `:focus-within` as well as hover.
* Accordions use `aria-expanded` / `aria-controls`; errors use `role="alert"`; decorative SVG is `aria-hidden`.
* Every content image has an `alt`; decorative hero and page-head images use `alt=""`.
* All motion is suppressed under `prefers-reduced-motion: reduce`.
* Tap targets are at least 44px in the header, menu and carousel controls.

---

## 7. Extending the system

1. **Adding a colour or size?** Add a token first, then use it. Never hard-code a value in a component rule.
2. **Adding a component?** Put it in `css/components.css` under a numbered banner comment, add it to the contents list at the top of that file, document it here, and add a live example to `pages/style-guide.html`.
3. **Page-specific tweak?** `css/pages.css`. If the rule would be useful on a second page, promote it to `components.css` instead.
4. **Adding a page?** Either copy an existing page and edit it, or add the route, meta and body to `tools/content.py` and re-run `python3 tools/build.py`. See `README.md`.
5. **Naming.** Loose BEM: `.block`, `.block__element`, `.block--modifier`. State classes are `.is-*` / `.has-*`. Utilities are `.u-*`. Behaviour hooks are `data-*` attributes so that renaming a class never breaks the JavaScript.
