# Botesdale Dental Practice & Implant Clinic — website

A static, dependency-free, fully responsive website. No build step is required to
run or deploy it: every page in this repository is plain HTML that a browser can
open directly.

---

## Quick start

```bash
# from the repository root
python3 -m http.server 8000
# then open http://localhost:8000
```

Opening `index.html` straight from the filesystem also works, though a local
server is closer to production behaviour.

---

## Structure

```
.
├── index.html                 Home
├── 404.html                   Not-found page
├── pages/                     Every other page, one folder deep
│   ├── about-us.html
│   ├── treatments.html
│   ├── general-dentistry.html …and its four child pages
│   ├── cosmetic-dentistry.html …and its six child pages
│   ├── preventative-dentistry.html …and its three child pages
│   ├── missing-teeth.html
│   ├── implant-clinic.html · implant-referrals.html
│   ├── referrals.html · fees-and-membership.html
│   ├── case-studies.html …and five case pages
│   ├── contact-us.html
│   ├── privacy-policy.html · cookie-policy.html
│   └── style-guide.html       Living component reference
├── css/
│   ├── base.css               Tokens, reset, typography, utilities
│   ├── layout.css             Wrap, grids, sections, header, footer
│   ├── components.css         Every reusable component
│   └── pages.css              Page-specific composition only
├── js/
│   ├── nav.js                 Header state, mobile menu
│   ├── ui.js                  Tabs, accordions, carousel, reveal, lightbox, cookies
│   ├── forms.js               Client-side validation
│   └── main.js                Small site-wide odds and ends
├── assets/images/
│   └── brand/                 favicon (photography goes in here too)
├── tools/                     Optional generator (see below)
├── design.md                  The design system
├── sitemap.xml · robots.txt · .nojekyll · .gitignore
```

Stylesheets are loaded in order — `base → layout → components → pages` — and
each later file may override the one before it. There is no `@import`, so there
is no request waterfall.

Paths are relative, with exactly two contexts: the root (`index.html`,
`404.html`) and `pages/`. That keeps the site portable — it works from a domain
root, from a subfolder, and from GitHub Pages project sites alike.

---

## Deploying to GitHub Pages

1. Create the repository and push this folder as the root.
2. **Settings → Pages → Source: Deploy from a branch**, branch `main`, folder `/`.
3. `.nojekyll` is already present, so folders and files are served as-is.

If you use a custom domain, add a `CNAME` file containing the domain, and update
`base_url` in `tools/content.py` plus the URLs in `sitemap.xml` and `robots.txt`.

---

## Editing

**By hand** — every page is readable HTML. Change the copy in place; the shared
header and footer markup is repeated in each file so nothing is hidden from you.

**With the generator** — `tools/build.py` assembles all 35 pages from
`tools/content.py`, which holds the site details, the navigation tree, the page
meta and the body content. Run:

```bash
python3 tools/build.py
```

It rewrites `index.html`, `404.html`, everything in `pages/`, and `sitemap.xml`.

> **Choose one.** Re-running the generator overwrites hand-edits. Either edit
> the HTML directly and stop using `tools/build.py`, or keep making changes in
> `tools/content.py` and re-run it. The generator exists because 35 pages share
> one header, one footer and one set of meta tags — it is the cheapest way to
> keep them identical.

Deleting `tools/` entirely leaves a perfectly good static site behind.

---

## Making the forms live

Four forms ship with full client-side validation and no back end:

| Page | Form |
|---|---|
| `contact-us.html` | General enquiry / new patient registration |
| `referrals.html` | CBCT & OPG referral, and the IRMER Service Level Agreement |
| `implant-referrals.html` | Patient self-referral, and dental professional referral |

The two referral pages are **multi-step**: their forms are split into panels
with a stepper across the top and Back / Continue below, and each panel is
validated before you can move on. The Service Level Agreement's list of
entitled people is a **repeat group** — "Add another person", with no fixed
ceiling of three — and it submits as an array:

```
sla-referrer[0][name]   sla-referrer[0][gdc]   sla-referrer[0][role]
sla-referrer[1][name]   …
```

Indices are always `0..n-1` with no gaps, whatever order people are added and
removed in. Whatever you wire the forms up to needs to expect that shape.

None of it depends on JavaScript to be usable: with JS off, every step is
visible, there is no stepper, the submit button sits at the end, and the
repeat group renders one person. Test that path before launch.

All the wiring is documented at the top of `js/forms.js`. In short:

* **Formspree** — set `action="https://formspree.io/f/XXXX" method="post"` on the
  `<form>` and delete the `e.preventDefault()` in the SUCCESS block.
* **Netlify Forms** — add `netlify` and a `name` attribute to the `<form>`.
* **Your own endpoint** — replace the SUCCESS block with a `fetch()` POST.

Validation stays as it is in all three cases.

> These forms collect patient-identifiable information. Whichever service you
> use must be covered by an appropriate data processing agreement, and the
> Privacy Policy should name it.

---

## Images

There is no photography in the build. Every media area is a grey placeholder
that names the shot belonging there:

```html
<div class="ph" role="img" aria-label="A family smiling together">
  <span class="ph__label">A family smiling together</span>
</div>
```

**To drop a real photograph in**, replace that whole `<div>` with an `<img>`:

```html
<img src="../assets/images/cards/family.jpg" alt="A family smiling together" loading="lazy">
```

Nothing else changes. The parent element already owns the aspect ratio and
`object-fit: cover`.

The hero and page heads are dark panels, not placeholders. Each has a
commented-out `<img>` in the markup showing exactly where its background
photograph goes, and a small "Hero photograph" marker in the corner — delete
the `<span class="ph-note">` once the image is in.

Suggested export sizes: hero and page-head backgrounds 1600–2000px wide;
strip tiles 900px wide at 4:3; cards and case images 900px wide at 3:2; team
portraits 760px wide at 3:4.

---

## Before launch — checklist

- [ ] Add the practice's photography in place of the grey placeholders
- [ ] Confirm the company registration number (currently `123456` from the brief)
- [ ] Confirm the fee guide — the price list is dated February 2022
- [ ] Have the Privacy Policy and Cookie Policy reviewed, and name the form processor
- [ ] Wire the forms to a real endpoint and test every one
- [ ] Set the real Facebook and Instagram URLs in `tools/content.py` → `SITE`
- [ ] Add Google Analytics or an alternative, and list it in the Cookie Policy
- [ ] Update `base_url` in `tools/content.py`, then regenerate `sitemap.xml`
- [ ] Check the Google Maps embed points at the right place
- [ ] Run Lighthouse and a link check on the deployed site

---

## Sitemap as built

Mirrors the client sitemap exactly. Two additions are marked.

```
Home
├── About us
├── Treatments
│   ├── General dentistry
│   │   ├── Root canal therapy
│   │   ├── Extractions
│   │   ├── Emergency dental treatment
│   │   └── Nervous patients
│   ├── Cosmetic dentistry
│   │   ├── Clear aligner
│   │   ├── Veneers
│   │   ├── Crowns
│   │   ├── Bridges
│   │   ├── Teeth whitening
│   │   └── Gum reshaping
│   ├── Preventative dentistry
│   │   ├── Check up
│   │   ├── Dental hygiene
│   │   └── Sensitive teeth
│   └── Missing teeth
├── Implant clinic
│   ├── Implant clinic      (the parent nav item links here)
│   └── Implant referrals
├── Referrals
├── Fees and membership
├── Case studies
│   ├── Treating worn dentition with composite bonding
│   ├── Replacement of missing teeth
│   ├── New upper denture
│   ├── Loose upper denture
│   └── Same day teeth
├── Contact us
└── Footer
    ├── Privacy policy
    ├── Cookie policy
    └── Style guide         (added — living design reference)
                            404 page (added)
```

The five case-study detail pages are not drawn on the client sitemap but exist
on the current website, so they have been carried across.
