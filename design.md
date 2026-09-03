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
| `--black` | `#1A1A18` | Ink. Headings, dark sections, solid buttons |
| `--black-2` | `#22292F` | Secondary dark ground — a second dark band, dark media panels |
| `--ink-rgb` | `26, 26, 24` | `--black` as channels, for `rgba()` scrims and shadows |
| `--paper` | `#F7F6F3` | The page ground |
| `--paper-2` | `#FFFFFF` | Pure white — a band, via `.section--paper-2`, and small lifts |
| `--paper-3` | `#EFEDE8` | Alternating section band |
| `--placeholder` | `#E5E3DC` | Image placeholder ground |
| `--placeholder-2` | `#DCDAD2` | Image placeholder on a tinted band |
| `--ink-soft` | `#5B615F` | Body copy on paper |
| `--ink-mute` | `#8A8F8C` | Meta, captions, placeholders |
| `--line` | `#D9D7D0` | Hairline on paper |
| `--line-dark` | `rgba(247,246,243,.18)` | Hairline on black |
| `--paper-soft` | `rgba(247,246,243,.70)` | Body copy on black |
| `--paper-mute` | `rgba(247,246,243,.50)` | Micro-labels on black |
| `--accent` | `#009EE3` | Arc motif, markers, focus, validation — from the logo artwork |
| `--accent-600` / `--accent-700` | `#008ECC` / `#006F9F` | `--accent-600` is the primary button's hover fill; `--accent-700` is the colour of a text link on paper |
| `--accent-800` | `#004F72` | The primary button's pressed border. Too dark to be a fill under an ink label — see §4.1 |
| `--ok` `--warn` `--error` | `#1D7A57` `#8A5A00` `#A93226` | Notices and form validation |

> **The brand blue is `#009EE3`, and it comes from the artwork.** The supplied logo files paint their accent in `#009EE3` — the wordmark and the icon's arc — so that is the practice's real blue, not the `#17A6DE` the design system previously approximated it with. The two differed by ΔE 8.7, well past the point of being distinguishable, and they sat inches apart in the header: the logo's own blue beside the accent on the nav arc and tab underline.
>
> The darker steps are the same hue scaled toward black, each picked against a constraint rather than by eye. **`--accent-600`** is the primary button's hover fill and must stay light enough to sit under an ink label (4.8:1, the same margin the old ramp had). **`--accent-700`** is a text link on paper, where `--accent` itself is only 2.8:1 (5.2:1). **`--accent-800`** is the pressed border only.
>
> One consequence worth knowing: `#009EE3` is *darker* than the accent it replaced (5.8:1 under an ink label against 6.3:1), so there is less room to darken before the label fails AA, and the primary button's hover step is correspondingly subtler than before.

**Dark grounds** for the hero and page heads: `--grad-hero`, plus `--grad-cool`, `--grad-warm`, `--grad-slate` if a gradient panel is ever needed. Media panels awaiting photography use `--placeholder` (see §4.4).

**Two blacks.** `--black` is the warm ink the whole site is set in; `--black-2` is a cooler, slightly lighter ground for a *second* dark surface — `.section--dark-2` and `.ph--dark` — so two dark sections in a row do not merge into one slab. `--dark` styling is unchanged by the variant; only the ground moves.

Every `rgba()` scrim and shadow derives from `--ink-rgb` rather than a hand-written triplet, so the ink is genuinely a single point of change. If you move `--black`, move `--ink-rgb` with it.

**Contrast.** Measured on the rendered page, not by eye:

| Pair | Ratio |
|---|---|
| `--black` on `--paper` | 16.1:1 |
| `--black-2` on `--paper` | 13.6:1 |
| `--paper-soft` on `--black` / `--black-2` | 8.4:1 / 7.4:1 |
| `--paper-mute` on `--black` / `--black-2` | 4.9:1 / 4.6:1 |
| Primary button ink label on `--accent` | 6.3:1 |
| …on `--accent-600` (hover) | 4.8:1 |

Two values moved *because* the ink moved, and both are load-bearing:

* **`--paper-mute` went from `.45` to `.50`.** At `.45` it measures 4.2:1 on `--black` and 4.0:1 on `--black-2` — under AA for the small uppercase meta it is used for. It was already failing at `.45` against the old ink (4.3:1); the new palette simply made it visible. `.50` clears 4.5:1 on both grounds.
* **`--accent-600` was lifted from `#1189BB` to `#128FC3`.** The primary button carries an *ink* label, so its hover fill has to stay light enough to sit under one. Against the old, darker ink `#1189BB` gave 4.8:1; against `#1A1A18` it gives 4.4:1 and fails. `#128FC3` restores 4.8:1 and still reads clearly darker than `--accent`.

`--accent` is only used for large text, borders and iconography — never for small body copy on paper.

### 2.1a Cache busting

Every local stylesheet, script and the favicon is linked with a `?v=<8-char md5>` of its own contents, computed at build time by `fingerprint()` in `tools/build.py`.

This is not an optimisation, it is a correctness fix. The files were previously linked as bare paths, so a returning visitor could load freshly deployed HTML against the stylesheet still sitting in their browser cache. That is not theoretical: it is exactly how the two-image brand mark shipped and rendered *twice, at full 648px width*, overflowing the viewport on a phone holding the previous `layout.css` — the markup was new, the rules that size and swap the two cuts were not there yet.

Hashing the content means any edit changes the URL, so the HTML and the CSS can never be a version apart. Nothing needs doing by hand; add a new stylesheet or script by routing it through `versioned()` alongside the others.

### 2.1b Container widths

| Container | Width | Use |
|---|---|---|
| `.wrap` | 1440 | **Only** where text and images sit side by side |
| `.wrap--narrow` | 900 | **All** text-only sections: prose, numbered steps, FAQs, benefit and price lists, the team grid |
| `.u-form-col` / `.form` | 680 | A form, and any copy directly above one |
| `.prose` / `.u-measure` | 640 | A single column of running prose |

1440 is a *side-by-side* width. A section that is only text — a run of numbered steps, an FAQ, a list of membership benefits — reads badly stretched across it.

The failure mode to avoid is capping the inner element while its heading stays on the 1440 line. That is what produced the ragged look on the fees page: `Your benefits include the following:` sat on the wide line while its list was centred at a 640 measure below, so the two had different left edges and the section read as two mismatched columns. **Cap the container, not the content** — then the heading and its content share one left edge, and centring the container is what moves the block, never centring the copy inside it.

**Do not cap twice.** Inside `.wrap--narrow` the container *is* the cap, so a `.prose` or `.u-measure` must not centre itself again — that was putting the copy 192px right of its own heading and reading as two mismatched columns. Those elements uncap inside a narrow container and line length is held by a measure on the paragraphs instead, so the block starts on the container's left edge, level with the heading. A `.form-block` is the same idea: it *is* the form column, so its heading sits on the same edge as its fields.

Copy that sits directly above a form is the same trap at smaller scale: a `--measure` intro above a `--form-col` form is centred to a different width, so the two start 20px apart. Use `.u-form-col`.

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

### 2.2a One size for running copy

Body copy had drifted to **seven** sizes across components doing the same job — 17px in `.prose`, 16px on bare paragraphs with no rule at all, 15px in `.ed`, 14px in `.p-row`, accordion panels, plan lists and team bios, 13px in strip captions. Same job, five different sizes.

The ladder is now:

| Token | px | Use |
|---|---|---|
| `--fs-lead` | 16 → 18 | An intro paragraph under a heading; the hero sub |
| `--fs-body` | 16 | **All running copy**, everywhere |
| `--fs-sm` | 14 | Copy inside a narrow grid tile (3–4 up), where 16 would not fit the column |
| `--fs-xs` | 13 | Meta, captions, field hints, form notes |
| `--fs-label` | 11 | Uppercase micro-labels |

If you are adding a component with a paragraph in it, it takes `--fs-body` unless it is a tile in a grid. Two specificity traps caught this: `.team__bio p` (0,0,1,1) silently beat `.team__gdc` (0,0,1,0), so the GDC line rendered as body copy rather than meta; and `.form__step-intro` had no rule of its own and borrowed `.field__hint`, so a step's intro rendered as a 13px grey hint.

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

**One primary per page, on any ground.** `c_cta()` renders the primary as `.btn--solid` whether the band is light or dark. It previously rendered as `.btn--light` on a dark band — the same treatment as the secondary — which left those pages with two equal-weight outline buttons and no primary at all. The accent fill with an ink label measures 6.3:1 on `--black`, so it carries the emphasis on dark as well as on paper. `demote=True` still drops the primary to an outline; that is for pages whose real primary action is a form further up, where a solid button in the closing band would compete with it.

**Full width on a phone.** Below 620px every `.btn` spans its column and `.btn-row` stacks. A 180px button floating in a 390px viewport reads as unfinished and is a worse tap target. `.btn--sm` is excluded — those are in-form utilities (Back, "add another") that belong inline.

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

### 4.2a Inline links in copy

A link sitting in running copy is always distinguishable from the text around it: ink, with a hairline `--accent-line` underline that goes full accent on hover.

**This is the default, not an opt-in.** `.link-inline` had to be remembered, and it was missed — a `tel:` link inside a `.notice` on the contact page fell through to the bare `a { color: inherit; text-decoration: none }` reset and rendered in body colour with no underline and no border, i.e. invisible as a link. The treatment now applies to any unclassed `<a>` inside a copy container (`.prose`, `.legal`, `.notice`, `.specs`, `.table`, a `.cta`/`.statement`/`.section-head` paragraph, a form note or hint). `:not([class])` keeps classed links on their own component styling, and `.link-inline` stays for links outside those containers.

On a dark ground the ink colour would disappear, so it flips to `--paper` there.

**The phone number is always a real link.** Left as plain text it is still tappable on iOS — Safari auto-detects phone numbers — but Safari styles it as a *native* link, which does not match the site and is why the number in a closing CTA looked wrong. `_linkify_phone()` turns the number in already-escaped copy into a proper `tel:` link, and `<meta name="format-detection" content="telephone=no">` stops iOS auto-linking anything else we have not linked deliberately.

### 4.3 Header & navigation — `layout.css` + `js/nav.js`

**The brand mark.** `assets/images/brand/` holds the supplied artwork: `-logo-` (wordmark plus icon, 648×77) and `-icon-` (the mark alone, 63×77), each in a black and a white cut, plus the favicon derived from the icon.

The mark is **three colours** — icon in `--black-2`, wordmark in `--black`, arc and dot in the brand blue — so it cannot be recoloured with `currentColor` or a CSS mask without flattening the blue to one tone. The header therefore ships both cuts as `<img>` and swaps them on `.is-scrolled` / `.nav--solid`; both are cached after the first page. The `<a>` carries the accessible name and both images take an empty `alt`, so the name is announced once rather than twice.

Transparent over the hero, then `.is-scrolled` swaps in a translucent paper background once the hero has passed. Desktop dropdowns open on hover and focus (`:focus-within`), so they are keyboard-reachable. Below 1080px the burger opens `.menu`, a full-screen sheet with focus trapping, Escape-to-close and expandable groups.

**The header scrim extends past the header, and eases.** It covers the nav plus 88px below it, holding its plateau to 66% so the falloff happens *below* everything it protects rather than across it — the same reason the team scrim holds a plateau behind its text. And it is smoothstep: it used to be `.88 → .55 at 60% → 0`, where the slope more than doubled at 60% of the header's height and drew a visible band straight across the sky on a photographic page head.

**Short plateau, long tail — the flat part is what reads as a band.** What looks like a hard black bar across the top of a photograph is the plateau, not the fade. So the plateau covers only what actually needs `.56` and everything below it is falloff: `.560` held to 60px — through the header and no further — then smoothstep across the remaining 160px, reaching nothing at 220px.

Those numbers come from `profile-topscrim.js`, which hides both scrims, screenshots the bare photograph and solves for the minimum alpha under each element rather than guessing: the nav links need `.540` and the header CTA `.475`, both inside y 15–57; the crumb row at y 85–104 needs `.415` at its worst over bright sky; nothing below that needs anything. The curve passes `.46` at the foot of the crumbs. The shape before it held `.560` all the way to 106px — 50px of flat ink no element had asked for. Same protection, roughly half the visible band.

One gradient stretched, not a second one added underneath — two overlapping curves of different shapes are what made the junction visible in the first place, and a photographic page head still carries no top gradient of its own.

It is also lighter than it was, `.56` rather than `.88`. That is measured, not eased off by feel: the nav links land at 4.65:1 over the brightest sky, the header CTA at 5.29:1, the crumbs at 4.94:1, and where the page title scrolls under the wordmark the mark still reads at 3.91:1 against the 3:1 a graphic needs. It cannot go to zero: with no top scrim at all the nav links measure **1.44:1** over that sky and the burger 2.70:1.

**A scrim sits behind the transparent header.** `.is-scrolled` does not arrive until the hero has almost passed, so hero copy scrolls underneath the transparent header well before it goes solid — the page title collided with the wordmark, white on white. `.nav::before` is a top-down gradient in `--ink-rgb` that keeps the transparent-over-hero look while guaranteeing anything sliding under the header is darkened before it reaches the logo; it fades out as the solid state fades in, and `.nav__inner` takes `position: relative; z-index: 1` so the header's own content paints above it.

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

**With a photograph (`.page-head--shot`).** `c_page_head()` renders the `<img>` only when the file is actually on disk — every page head is written with an `image` argument, but the hero photography mostly does not exist yet, so rendering it unconditionally would give 34 pages a broken reference. Without a file it keeps the commented placeholder.

**The dark belongs at the bottom, and nowhere else.** A photographic head carries one scrim of its own, rising from the foot behind the label, heading and sub; the top is left to `.nav::before` (§4.3), which is already there for every page and now covers the crumbs with it. The single `.62 → .28 → .86` ramp it replaced muted the whole image *and* reversed slope at 40%, which creases visibly over a photograph. It is smoothstep, for the reason given in §4.13.

**A photograph needs room to be a photograph.** The scrims are sized by the content they protect, and that content is a fixed pixel height — so on the 396px head the header scrim took the top 41% and the copy plateau the bottom 58%, leaving **1% of the picture untouched**. That, not the opacities, is what was muting the image. `.page-head--shot` is therefore `min(74vh, 660px)`, and `min(80vh, 620px)` below 720px: same content, same protection, far more picture. And `saturate(.85) contrast(1.02)` now applies only to heads *without* a photograph — it was there to tame the placeholder gradients, and a real image does not want it.

**The values are measured, not guessed.** Against the lightest pixel actually behind each element on the about-us photograph, the minimum scrim needed is `.54` for the h1, `.69` for the sub, `.50` for the nav links and — up at the top, where the crumbs now sit — `.415`. The plateau is `.68` and holds to 32% of the head, reaching nothing by 56%. It came down from 38% when the crumbs moved to the top: they had been the topmost thing the foot had to protect. What the header scrim gained in tail, the foot gave back.

**`--paper-mute` cannot be used over a photograph.** At 50% white on a bright pixel it needs a `.86`–`.92` scrim to reach AA — effectively blacking the picture out — against `.42`–`.56` at full paper, and every point of scrim is a point of picture lost. So on `--shot` the label **and sub** go to `--paper` (the crumbs are full paper on every head now — §4.7); taking the sub with them is what let the plateau drop from `.75` to `.68` and stop well short of the 58% it used to reach. The soft tones exist for a flat dark ground; over a photograph the hierarchy comes from size and weight instead, and legibility wins.

That override block has to sit **after** the base `.page-head .label` / `.page-head p` rules, not before them: `.page-head--shot p` and `.page-head p` are the same specificity, so on the earlier source position the sub silently kept `--paper-soft` and measured 3.80:1.

The suite hides the text, screenshots the head, decodes the PNG and samples the pixels where each element sat — so contrast is checked against the real composite of photograph plus both scrims, not against an assumption.

The compact hero used on every inner page. Same structure as `.hero`; add `--short` for legal pages. Carries the breadcrumb and, where it is not simply a repeat of the `h1`, a micro-label.

**The crumbs sit at the top of the head, not on the title block.** They answer where-am-I; the label, `h1` and sub are one unit and read better without a line of meta above them.

```html
<div class="page-head__inner wrap">
  <div class="page-head__top">…crumbs…</div>
  <div class="page-head__title">…label, h1, sub…</div>
</div>
```

`.page-head` is `align-items: stretch` so the inner spans the head; the inner is a flex column, and `.page-head__title` takes `margin-top: auto` to fall to the foot. **In flow, not absolute.** An absolute crumb row is outside the box model, so the title below cannot see it: on a `--short` legal head the label rode straight through the crumbs, and a four-level trail wrapping to three lines at 390px did the same on eight treatment pages. `margin-top: auto` costs nothing when there is slack above and yields when there is not.

`verify-crumbs.js` sweeps all 33 page heads at 390 / 768 / 1440 and asserts three things: the crumbs are above the title block with no overlap, both start on the same rail, and no `.crumbs` is left inside `.page-head__title`. The overlap check is the one that earns its place — it is what caught both collisions.

### 4.7 Breadcrumb — `.crumbs`

Uppercase, 11px, with a `/` separator. `--on-paper` variant for use outside a dark page head (currently unused — nothing emits it).

**One tone, at full strength; links are marked by an underline, never by dimming.** It used to run the other way — links at `--paper-mute` / `--ink-mute` with the current page at full strength — so the item you *can* click was the faint one and the item you are already on was the loud one. That reads as a disabled link.

Both muted tones were also failing where it counted. `--ink-mute` is **3.04:1** on paper, under AA outright. And over a bright sky `--paper-mute` needs a **`.86`** scrim to reach 4.5:1 — it would black out the photograph the head exists to show (§4.6). There is no scrim budget for a translucent white in the crumb row, so the trail is `--paper` on dark and `--black` on paper, and `.crumbs a` inherits it. Hover and `:focus-visible` bring in an underline via `text-decoration-color`, so nothing reflows.

`verify-crumbs.js` asserts the link's computed colour equals the trail's, and that no part of the trail is translucent.

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

### 4.8a Band arc — `.band-arc`

The smile standing on its own at the foot of a closing band (`.cta`, `.statement`), about a third of the container, centred, drawn in on scroll.

It carries its own `[data-reveal]`, so the existing observer adds `.is-in` and the stroke runs from `stroke-dashoffset: 100` to `0`. `pathLength="100"` makes that dash arithmetic independent of the path's real length, so the curve can be edited without retuning the animation. Unlike `.arc` it keeps its aspect ratio — no `preserveAspectRatio="none"` — so it reads as the motif rather than a stretched rule.

Putting `[data-reveal]` on the arc rather than on the section matters: `[data-reveal]` starts at `opacity: 0`, so anything carrying it is invisible until scripting runs. The arc is decorative and `aria-hidden`, so with scripting off it simply never appears and no copy is at risk.

### 4.9 Strip grid — `.strip`

Hairline-separated tiles, 2–4 up, with a 4:3 media panel that desaturates until hover. Set the count with `.strip__row--2` / `--3`, default 4.

### 4.10 Card — `.card`

A bordered tile for grids that need visible gaps rather than hairline seams. `--dark` variant available.

### 4.11 Statement band — `.statement`

Full-width dark section for a single idea, with optional `.facts` beneath it. **Centred** — heading at `22ch`, copy at `56ch`, the facts grid and any link centred under them (§1.5). Use `.facts--paper` for the same component on a light ground; that variant is unaffected outside a `.statement`.

**An odd number of facts on a phone.** The grid is `auto-fit`, which settles at two columns on a phone, so an odd count strands the last fact alone in the left-hand column. Below 620px the count is pinned to two — so the behaviour is deterministic rather than dependent on how the `auto-fit` maths falls — and `.fact:last-child:nth-child(odd)` spans both columns. The band is centred, so the orphan centres under the pairs.

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

Name and role are white over the foot of the portrait; the biography reads underneath at full card width. The scrim (`.team__portrait::after`) **holds full strength behind the text, then eases away on a smoothstep curve.** The plateau is set by contrast; the shape of the falloff is set by appearance.

*Contrast.* The text sits inside the plateau, so its legibility never depends on what the photograph is doing. Opacity is **`.75`**, chosen against the worst case — a blown-out white image — where the name reads 9.6:1 and the role label 5.7:1. The label is the binding constraint, not the name: it is `--paper-soft`, a *translucent* white, so it composites onto the scrim rather than sitting on it. The floor is around `.70`; `.75` keeps margin without burying the picture, which `.88` did.

*Appearance.* This was a flat zone meeting a **straight ramp**, and it read as a hard-edged black band. The reason is rate, not opacity: a linear ramp starts with a non-zero slope, so the junction is an abrupt change in how fast the darkness falls off, and the eye finds that instantly. **Smoothstep has zero slope at both ends**, so it leaves the plateau at the same rate the plateau was going — nothing — and the two blend invisibly. The tail runs long (to 80%) so the falloff never bunches into an edge either.

The suite evaluates the declared gradient at the positions the name and role *actually* occupy, and caps how fast alpha may change per 1% of height, so neither the contrast nor the smoothness can regress unnoticed.

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

### 4.22 Prev / next pager — `.pager`

Two links at the foot of a page: the previous and next page in its section, built by `c_group_pager()` from the same `GROUPS` ordering the sidebar rail used to render.

**This replaced the rail.** A sticky column of sibling links competed with the copy for the whole scroll and cost the content a 260px column on every treatment and case-study page. The pager says the same thing once, at the point it becomes useful — when the reader has finished. It sits after the content and before the closing CTA band.

Two links share the row evenly at every width, titles wrapping inside their own half and centred — stacking them full width on a phone made a two-step sequence read as two unrelated blocks. A single link (first or last in a sequence) takes the whole row via `.pager__item:only-child`, rather than sitting in one half with the other left as bare background.

**Only where there is a real sequence.** Hub and overview pages take none — they are the top of a section, not a step in it — and neither do the implant pages: clinic, referrals and missing teeth are related but not ordered, so a "next" between them would be invented rather than navigational.

### 4.24 Forms — `.form`, `.field` + `js/forms.js`

**The submit needs more room than a field.** `.form__actions` sits outside `.form__grid`, so the grid's own `--s-6` row gap does not reach it. It carried only `--s-2`, which put the button 8px under the consent checkbox while every field above was separated by 24 — the action looked attached to the last field rather than being the end of the form. It now takes `--s-8`. The note below keeps a tighter `--s-4`: it belongs to the button rather than standing apart from it, so the spacing groups them.

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
