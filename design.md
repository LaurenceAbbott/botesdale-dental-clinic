# Botesdale Dental — Design System

Version 1.0 · Living document
Reference implementation: **`pages/style-guide.html`** (open it in a browser — every component below is rendered there)

---

## 1. Principles

The reference for this system is precision-engineering brand design — Porsche in particular. That translates into five working rules:

1. **One rail.** Every piece of text on the site — inside a centred container or inside a full-bleed section — starts or stops on the same vertical line. Media is the only thing allowed to cross it. See §2.3.
2. **Lines, not boxes.** Structure is expressed with 1px hairlines and alignment. Shadows are almost never used; corners are square (`--radius: 0`). **Form controls are the deliberate exception** — an input is a thing you put something into, and it has to look like one, so fields are bordered boxes (§4.24). The border is the same hairline and the corners are still square, so they sit inside the system rather than beside it.
3. **Two grounds.** A warm off-white (`--paper`) and a near-black (`--black`). Every section belongs to one of them. Dark sections are used deliberately, for emphasis, roughly one per screenful of scrolling.
4. **One accent, sparingly.** `--accent` appears in the arc motif, list markers, focus rings, validation, text links (§4.2) and the fill of the one primary button a page is allowed (§4.1). It is never used as a background for large areas — a button is the largest thing it fills.
5. **Editorial rhythm.** Full-bleed media/copy splits, generous vertical space, and a short uppercase micro-label above almost every heading. **Copy is left-aligned on the rail by default, with three deliberate exceptions**: the quote (§4.14), the statement band (§4.11) and the closing CTA (§4.25) are centred. Those three are single voices or single ideas rather than passages to work through, and left-aligning them at a 24–54ch measure inside a 1440 container put all the empty space on one side. Centring them punctuates a page that is otherwise on the rail — which only works because it is three moments, not a default. Anything you read *through* stays left.
6. **Restrained motion.** 200–480ms, ease-out, and only on hover, reveal and open/close. Everything respects `prefers-reduced-motion`.

### The arc

The practice's signature motif is a shallow arc — a smile. It appears in two places:

* **`.arc`** — an inline SVG stroke that draws itself in under nav items, footer links and tabs on hover. It is a decoration on things that already read as navigation, never the only signal that something is a link — see §4.3. On a device that cannot hover, tapping one of these links draws the arc and the navigation waits for it; see §4.3a.
* **`#heroArc`** — an SVG `clipPath` on the bottom edge of the dark hero and page-head panels, so each one ends in a smile rather than a straight line.

Both are defined once per page (`<svg class="svg-defs">`). If you remove the `svg-defs` block, the hero panels go back to a straight bottom edge. It once also held `#smileClip`, which clipped a sweeping fill across buttons on hover; that is gone (§4.1).

The arc is **cut into** the panel rather than drawn on top of it, so whatever is behind shows through the curve — which is the page ground, since the panel still occupies its full height in layout. That means the section following a hero has to be on `--paper` (or have no background of its own). Every page currently satisfies this; if you ever put a `--paper-3` band directly under a page head, the sliver revealed by the arc will be the wrong colour.

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
| `--accent-600` / `--accent-700` | `#1189BB` / `#0B6E97` | `--accent-600` is the primary button's hover fill; `--accent-700` is the colour of a text link on paper |
| `--accent-800` | `#08506E` | The primary button's pressed border. Too dark to be a fill under an ink label — see §4.1 |
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

`--wrap` (1440px) is the maximum width of any line of text on the site. A centred `.wrap` puts its content at `(100vw − 1440) / 2 + --pad-inline` from the viewport edge; that line is **the rail**, and everything textual aligns to it.

**Nothing bleeds to the viewport edge any more.** The editorial block used to run its media right off the side of the screen; it now overhangs the rail by a fixed *tenth of the outer margin* and stops. The margin is split 90 / 10 and the picture is allowed into the inner tenth only:

```css
--col-half: minmax(0, calc(var(--wrap) / 2 - var(--pad-inline)));

.ed {
  grid-template-columns:
    minmax(calc(var(--pad-inline) * .9), 9fr)   /* outer margin, 90%     */
    minmax(calc(var(--pad-inline) * .1), 1fr)   /* overhang lane, 10%    */
    var(--col-half) var(--col-half)
    minmax(calc(var(--pad-inline) * .1), 1fr)
    minmax(calc(var(--pad-inline) * .9), 9fr);
}
.ed__media { grid-column: 2 / 4; }   /* overhangs the rail, stops at the centre */
.ed__text  { grid-column: 4 / 5; }   /* ends on the rail                        */
.ed--rev .ed__media { grid-column: 4 / 6; }
.ed--rev .ed__text  { grid-column: 3 / 4; }   /* starts on the rail             */
```

The `9fr : 1fr` split means the overhang is always a tenth of whatever margin the viewport happens to have — 13px at 1600px, 43px at 2200px — so it stays proportionate instead of turning into a bleed on a wide screen. The matching `.9 / .1` *minimums* keep the ratio holding below the container width too, where there is no free space to distribute; the two lanes still add up to `--pad-inline`, so the rail itself never moves.

Because the outer lanes are `fr` and the content columns are capped, the text column lands on exactly the same pixel as a centred `.wrap` at every viewport width — and the measure inside it stays constant as the window grows. No `100vw` arithmetic is involved, so there is no scrollbar-width error.

`.ed` also carries `padding-block: var(--section-y)`, so consecutive blocks — and a block against the dark band below it — are separated by paper rather than butting together.

Two things to know if you extend this:

* Give every child of the grid `grid-row: 1`. Without it, an item whose column starts *before* the auto-placement cursor is pushed onto a second row — which is what silently breaks reversed blocks.
* Below 860px the grid collapses to one column and `.ed` itself takes `padding-inline: var(--pad-inline)`.

### 2.4 Spacing

A 4px base scale: `--s-1` (4px) through `--s-12` (112px). Section padding uses the fluid `--section-y` / `--section-y-tight` tokens rather than a fixed step, so vertical rhythm scales with the viewport.

Layout tokens: `--wrap` (1440px), `--wrap-wide` (1440px — currently the same, and `.wrap--wide` is unused), `--measure` (640px), `--gutter`, `--pad-inline`, `--pad-block`, `--nav-h` (73px), `--control-h` (48px).

`--control-h` is the height of every single-line form control. It is fixed rather than left to each input's intrinsic sizing because date and time inputs size themselves from their own internal rendering and will not match a text input — Chromium makes them a couple of pixels taller, Safari collapses an empty one well below the rest. Pinning both to one token is the only thing that holds on both engines, and it keeps every field above the 44px tap-target minimum.

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
| `≤ 720px` | Stepper labels give way to the step count and the panel's own heading |
| `≤ 620px` | `.cols-*` → 1 column |
| `≤ 540px` | Strip → 1 column |
| `≤ 479px` | Buttons in a `.btn-row` go full width |

---

## 4. Components

Each entry lists the file it lives in, the markup, and the modifiers available. All of them are rendered live in `pages/style-guide.html`.

### 4.1 Button — `components.css`

```html
<a class="btn btn--solid" href="#"><span class="btn__label">Book a visit</span></a>
```

**There is no sweep.** A fill clipped to the arc used to slide across on hover. It was driven entirely by `:hover`, so on a touch screen it never ran — and iOS keeps `:hover` after a tap, which left the arc frozen part-way across the button. Buttons change colour now. `#smileClip` had no other user and has gone from the shared defs.

**One primary per page.** `--solid` is the primary and a page gets one: the single thing you most want the visitor to do. Where a page carries a form, the form's submit is that primary and the closing CTA is demoted — `c_cta(..., demote=True)` renders its leading button as an outline. Where a page carries two forms, the secondary one is built with `f_form(..., variant='outline')`, which also carries through to the wizard's *Continue* via `data-step-variant`, so a stepped form never shows a primary the page has not allotted it. The style guide is the one exception: it is a component reference and has to show every variant at once.

| Modifier | Ground | Rest | Hover | Press |
|---|---|---|---|---|
| `--solid` | paper or dark | `--accent` + ink label — 6.8:1 | `--accent-600` — 4.8:1 | `--accent-600`, border `--accent-800` |
| `--outline` | paper | none, ink border | inverts to ink | — |
| `--light` | dark only | none, paper border | inverts to paper | — |

**Why the label is ink and not white.** White on `--accent` is **2.78:1** — it fails AA badly, and at 13px there is no large-text exemption to fall back on. Ink on `--accent` is 6.8:1.

**Why press darkens the border, not the fill.** The ink label is what limits the range. It needs a fill of at least L 0.2 to clear 4.5:1, and the steps go:

| Fill | Ink label | White label |
|---|---|---|
| `--accent` `#17A6DE` | **6.80:1** | 2.78:1 |
| `--accent-600` `#1189BB` | **4.79:1** | 3.95:1 |
| `--accent-700` `#0B6E97` | 3.32:1 | **5.69:1** |
| `--accent-800` `#08506E` | 2.15:1 | **8.81:1** |

So an ink label has exactly one darker step available. Hover takes it, and press darkens the border instead — pressed still reads as pressed, and the label never drops under contrast. Going darker than `--accent-600` would mean flipping the label to white mid-interaction, which is worse than a border change.

Also `--sm`, `--block`, `.is-disabled`. Wrap groups in `.btn-row`.

### 4.2 Arc link — `components.css`

The standard "read more" affordance.

```html
<a class="arc-link" href="#">Read more</a>
```

**It no longer carries an arc.** The name is kept because 40-odd usages reference it, but the motif has gone: the arc was drawn in on hover, and hover does not exist on a touch screen, so on a phone the link was a line of grey uppercase text with nothing at all to say it was a link. It is now an ordinary link — accent coloured, underlined, sentence case — legible as one without any interaction.

* On paper it uses `--accent-700`, not `--accent`: 5.3:1 against 2.2:1, which is the difference between passing AA at this size and failing it. Hover goes to `--black` — `--accent-600` is *lighter* than `--accent-700`, so the obvious hover token would drop the link to 3.6:1.
* `--light` for dark grounds uses `--accent` at 6.8:1, hovering to `--paper`.
* `.statement .arc-link` has to restate the colour because it out-specifies the modifier.
* Two usages are `<span class="arc-link">` inside a card that is itself a link — affordance text rather than a nested link. They take the same styling.

The general rule this follows: **hover may enhance an affordance, never carry it.** The arc is still right on nav and footer links, which read as navigation from their position; it was wrong as the only cue on a standalone call to action.

### 4.3a Letting the arc finish before the page changes — `js/ui.js`

On the links that kept the arc, a tap on a touch device would previously navigate before the arc drew at all, so the motif was invisible to anyone without a mouse. Tapping one now draws the arc and holds the navigation until it finishes.

A delayed navigation is a slower navigation, so this is deliberately narrow. It is skipped — the click is never cancelled — when any of these hold:

| Condition | Why |
|---|---|
| The arc has already drawn | On a hovering pointer it finished before the click landed; there is nothing to wait for, so **desktop is never delayed** |
| `prefers-reduced-motion` | No animation to wait for |
| Modifier or middle click | The browser is about to open a tab; never interfere |
| Off-site, `tel:`, `mailto:`, `download` | Not a page transition |
| A link to the current page | Nothing is opening |
| No `.arc` inside the link | Nothing to draw — this is what exempts `.arc-link` |

In practice the wait only happens on touch and keyboard, where it doubles as feedback that the tap registered. It is capped at 400ms and backed by a timer as well as `transitionend`, so a transition event that never arrives cannot strand someone on the page they tried to leave. The click is only cancelled once every check above has passed, so if the script fails the links stay ordinary links.

Set by adding `.is-arcing` to the link, which draws the arc the same way `:hover` does.

### 4.3 Header & navigation — `layout.css` + `js/nav.js`

Transparent over the hero, then `.is-scrolled` swaps in a translucent paper background once the hero has passed. Desktop dropdowns open on hover and focus (`:focus-within`), so they are keyboard-reachable. Below 1080px the burger opens `.menu`, a full-screen sheet with focus trapping, Escape-to-close and expandable groups.

**The header CTA's label follows its border.** `.nav__cta` is paper-on-transparent over the hero. When `.is-scrolled` swaps in the paper background, the rule that flips the border to `--black` has to flip `color` with it — otherwise the label stays paper on paper and the button reads as an empty box.

**The sheet has no rules between its items.** It used to: every `.menu__link` carried a `border-bottom`, but the link is `width: fit-content`, so each rule stopped at the end of its own text while `.menu__group` ran the full width — a ragged mix of stub and full-width lines down the sheet. They were separating items that 26px type and 18px of padding already separate. Sub-items are indented by `--s-5` instead, which does the hierarchy the rules were failing to. This is the exception that proves §1.2: a hairline earns its place by doing work no other means does. Down a list of large type in open space, it does none.

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

The bottom edge is clipped to the arc (`clip-path: url(#heroArc)`, §1). The path lifts the two bottom corners to `0.955` of the panel height and holds full height at the centre, so the curve only ever eats into the corners — and `.hero__inner` / `.page-head__inner` carry one extra step of bottom padding because the copy sits in a corner the arc lifts.

**If you are grading the photograph:** the arc reads because the panel is at its darkest exactly where the curve is. A gradient that fades the image *out* toward the bottom will wash the curve away against the paper; the scrim already runs the other way (transparent at the top, `.82` black at the bottom), which is what makes the edge crisp. Fade in from the top, not out at the bottom — and if your image carries its own gradient, turn the scrim down rather than stacking the two.

### 4.6 Page head — `components.css`

The compact hero used on every inner page. Same structure as `.hero`; add `--short` for legal pages. Carries the breadcrumb and, where it is not simply a repeat of the `h1`, a micro-label.

### 4.7 Breadcrumb — `.crumbs`

Uppercase, 11px, with a `/` separator. `--on-paper` variant for use outside a dark page head.

### 4.8 Editorial block — `.ed`

The workhorse: a media panel overhanging the rail beside a copy column (§2.3).

```html
<section class="ed ed--cols" data-reveal>
  <div class="ed__media"><div class="ph">…</div></div>
  <div class="ed__text">
    <span class="label">Philosophy</span>
    <h2>…</h2>
    <div class="ed__body ed__body--cols"><p>…</p><p>…</p><p>…</p></div>
    <a class="arc-link" …>…</a>
  </div>
</section>
```

**Modifiers:** `--rev` (media right, copy starts on the rail), `--warm` (a half-step darker placeholder, for tonal alternation between consecutive blocks), `--cols` (see below).

**Two-column copy.** Three paragraphs or more in a half-width column runs long and thin and leaves the rest of the row empty, so `c_ed()` adds `.ed--cols` / `.ed__body--cols` automatically at that length: the heading uncaps to the full column and the paragraphs run two up beneath it, collapsing back to one column under 1100px. The body is a grid rather than `column-count` so a paragraph is never split across the gutter — and the grid owns the vertical rhythm, because the global `p + p { margin-top }` would otherwise push the second paragraph 16px below the first and stop the columns lining up.

### 4.9 Strip grid — `.strip`

Hairline-separated tiles, 2–4 up, with a 4:3 media panel that desaturates until hover. Set the count with `.strip__row--2` / `--3`, default 4.

### 4.10 Card — `.card`

A bordered tile for grids that need visible gaps rather than hairline seams. `--dark` variant available.

### 4.11 Statement band — `.statement`

Full-width dark section for a single idea, with optional `.facts` beneath it. **Centred** — heading at `22ch`, copy at `56ch`, the facts grid and any link centred under them (§1.5). Use `.facts--paper` for the same component on a light ground; that variant is unaffected outside a `.statement`.

### 4.12 Process list — `.p-row`

Numbered hairline rows (`01`, `02`, …). The default way to explain a sequence.

### 4.13 Team card — `.team__card`

Headshots side by side inside `.wrap`, two up (one up under 860px). These are portraits, not landscape scenes: a full-bleed alternating row wasted the width and squeezed each biography into a thin column.

```html
<ul class="team__grid" role="list">
  <li class="team__card">
    <div class="team__portrait">
      <div class="ph">…</div>
      <div class="team__id"><h3>Dr Martin Sulo</h3><span class="label">Dental Surgeon</span></div>
    </div>
    <div class="team__bio"><p>…</p><p class="team__gdc">GDC No: 84351</p></div>
  </li>
</ul>
```

Name and role are white over the foot of the portrait; the biography reads underneath at full card width. The scrim (`.team__portrait::after`) is **flat at the bottom, not a plain ramp** — `rgba(0,0,0,.88)` held solid for the bottom 26% before fading out at 52%. The overlaid text sits entirely inside that flat zone, so it keeps 6.2:1 whatever the photograph does behind it; a straight linear fade would put the label at roughly 2:1 over a bright background.

### 4.14 Quote & carousel — `.quote`, `[data-carousel]`

A single quote renders statically; more than one becomes a carousel that auto-advances every 8 seconds and pauses on hover or focus. Dots are generated by `js/ui.js`. **Centred**, with the measure capped at `26em` so a long testimonial still reads as a column rather than a wall, and the carousel controls centred under it. A testimonial is one voice, not a passage — see §1.5.

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

**It sits on the left and it looks like a menu.** `.with-rail` is `260px minmax(0, 1fr)` and the rail comes *first in the DOM*, so focus order matches what you see. `.rail__list` is a bordered card on `--paper-2` with each link a padded row — a loose column of links to the right of the copy did not read as navigation at all.

### 4.23 Pager — `.pager`

Previous / next split used between case studies.

### 4.24 Forms — `.form`, `.field` + `js/forms.js`

Bordered fields on `--paper-2`, uppercase micro-labels above, and a `.field__error` element that fills in on validation failure.

Fields are boxes, not underlines. An underline leaves the start and the end of the input implicit, and a column of them reads as a stack of rules with text floating between — you cannot tell at a glance where a field begins, or that it is a field at all. Boxes also mean the form carries **one** horizontal rule (above the action row) instead of one per field, so the remaining lines actually mean something. Hover darkens the border; focus turns it accent with a 3px `--accent-tint` ring; `.has-error` and `.is-valid` recolour the whole border rather than one edge.

Spacing is uniform: `--s-6` between fields, `--s-2` between a label and its control, `--s-6` above a `.form__section-title`. Nothing in a form should need a bespoke margin.

```html
<div class="field">
  <label for="c-name">Your name <span class="field__req">*</span></label>
  <input id="c-name" name="c-name" type="text" required>
  <span class="field__error" role="alert"></span>
</div>
```

Add `data-validate` and `data-success="<id>"` to the `<form>`. Validation runs on submit, and on blur once a field has been touched. States: `.has-error`, `.is-valid`. Choice controls use `.choice` / `.choice-grid`; long forms are divided with `.form__section-title`.

**One column, always.** `.form__grid` is a single column at every width. A form is a sequence to be worked through top to bottom; a second column asks the eye to pick a path and makes the order ambiguous — worse still when a field's label sits beside an unrelated one. `.field--full` and `.form__grid--single` remain as harmless aliases. Two forms on one page stack in a `.form-stack`, separated by a rule, rather than sitting side by side.

### 4.24a Multi-step form — `[data-steps]`, `.stepper`, `.form__step`

Long forms are split into panels. Each panel is a `[data-step]` with a `data-step-title`; `js/forms.js` builds the stepper and the Back / Continue row, shows one panel at a time, and validates the current panel before letting you advance.

```html
<form class="form" data-validate data-steps data-success="xSuccess" novalidate>
  <div class="form__step" data-step data-step-title="Patient details">
    <div class="form__section-title">Patient details</div>
    <div class="form__grid">…</div>
  </div>
  …
  <div class="form__actions">…submit…</div>
</form>
```

Everything the wizard needs is generated, so **the markup degrades cleanly**: with JavaScript off, every panel is visible, there is no stepper, and the submit button sits at the end of one long form. Nothing is behind a step that a non-JS visitor cannot reach.

* Only steps already reached are clickable in the stepper; jumping ahead would skip validation in between.
* Submitting validates every step, not just the visible one, and reveals the step holding the first error.
* Enter advances instead of submitting, except on the last step (and never when a button has focus).
* The step title is shown once: by the stepper's labelled list on desktop, by the panel's own `.form__section-title` below 720px where that list is hidden.

Use it when a form runs past roughly fifteen fields. Below that the steps cost more than they save.

### 4.24b Repeat group — `[data-repeat]`

A variable-length list of identical field sets — "add another entitled person". The first item is in the markup and the rest are cloned from a `<template>`, so a non-JS visitor still gets one usable item.

```html
<div class="repeat" data-repeat data-repeat-name="sla-referrer"
     data-repeat-singular="Person" data-repeat-min="1" data-repeat-max="12">
  <div class="repeat__list" data-repeat-list>
    <div class="repeat__item" data-repeat-item>…</div>
  </div>
  <template data-repeat-template>…the same item, with __i__ / __n__ …</template>
  <button data-repeat-add>…</button>
</div>
```

Controls are named `base[i][suffix]` with ids `base-i-suffix`, so a back end receives a clean array rather than `referrer1`, `referrer2`, `referrer3`. On every add and remove the script renumbers `id`, `name`, `for` and `aria-*` so the indices stay `0..n-1` with no gaps, and refreshes each item's visible number. Remove disappears at `min`; Add disappears at `max`. Both actions move focus somewhere sensible and are announced through a visually hidden live region.

In the generator, build one with `f_repeat()` — it takes a function returning the fields for one item and uses it for both the first item and the template, so the two cannot drift apart.

### 4.24c Chooser — `[data-chooser]`, `.chooser`

A tab switcher for a page that carries one form per audience, where nobody needs to see both. Used on `implant-referrals.html` to separate the patient self-referral from the dental professional referral.

```html
<div class="chooser" data-chooser>
  <div class="chooser__tabs" role="tablist" aria-label="Who is referring?" hidden>
    <button class="chooser__tab" role="tab" data-chooser-key="patient"
            id="implant-tab-patient" aria-controls="implant-panel-patient"
            aria-selected="true" tabindex="0">…</button>
    …
  </div>
  <div class="chooser__panel" id="implant-panel-patient" role="tabpanel"
       aria-labelledby="implant-tab-patient" tabindex="0">…</div>
</div>
```

The tab row ships **hidden** and every panel ships **visible**; `js/ui.js` unhides the tabs and takes over. So with JavaScript off the page is two headed forms one after another — the component never hides anything until it can also offer a way back.

* Standard tablist keyboard behaviour: arrows move, Home / End jump, roving `tabindex` keeps the group to one tab stop.
* The selected key is written to the URL hash, and `#patient` / `#professional` on arrival opens that tab — so links can point at the right form.
* Enhanced, each panel's own `<h2>` is visually hidden (it would repeat the tab), but stays in the accessibility tree and the document outline.

The tabs are **boxed**, not underlined, on purpose: an underlined tab row directly above the stepper's underlined progress bar reads as one confused set of lines. A chooser is a choice, not a position.

### 4.24d Section split — `.section-split`

Two equal columns: a `.section-head` on the left, the content that belongs to it on the right. The answer to a section whose heading and short intro leave the right half of a 1440 container empty. Collapses to one column under 900px.

### 4.25 CTA band — `.cta`

**Centred** closing block — heading at `20ch`, copy at `52ch`, buttons centred. One per page, at the end, and the only place the eye is asked back to the middle after a page of left-aligned content. `--dark` inverts it.

### 4.26 Cookie banner — `.cookie` + `js/ui.js`

Slides up after 900ms unless a choice is already stored in `localStorage` under `bdp-cookie-choice`. Storage access is wrapped in `try/catch` for private-browsing mode.

### 4.27 Back to top — `.to-top`

Appears past 700px of scroll.

### 4.28 Tab nav — `.tabnav` / `.tab` + `js/ui.js`

Sticky in-page jump bar with an `IntersectionObserver` scroll-spy. Sits directly beneath the header (`top: var(--nav-h)`).

### 4.29 Reveal on scroll — `[data-reveal]`

Add the attribute to any element; `js/ui.js` adds `.is-in` when it enters the viewport. `data-reveal-delay="1|2|3"` staggers a group. Disabled entirely under `prefers-reduced-motion`.

---

### 4.30 Two columns, and when not to use them

`.cols-2` is for **peers** — three treatment cards, two plan cards, a row of the same kind of thing. It is not a way to fit two unrelated blocks onto one screen.

Putting an `h2` in each column gives a reader two things at the same level and no order to read them in, and it halves the measure of whatever passage is in there. The fees page had two such sections, with the plan cards nested in a *second* two-column grid inside the right-hand one — so each card got a quarter of the page and the price collided with its own unit. The case studies intro paired a passage with a testimonial and squeezed the copy to about five words a line by the middle breakpoints.

Both are single column now, laid out as a vertical narrative: one idea per band, each with its own `.section-head`, alternating `--paper` and `--paper-3`, with a `.statement` where a single number or sentence deserves the whole width.

The test before reaching for `.cols-2`:

* **Are the two columns the same kind of thing?** If not, they are bands, not columns.
* **Is either column a passage to read?** Long-form copy wants `--measure`, and half of a `.wrap` is narrower than that below about 1400px.
* **Does each column need its own heading?** Two `h2`s side by side have no reading order.

A page is allowed to be tall. Vertical space is free; horizontal space is not.

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
