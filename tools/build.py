#!/usr/bin/env python3
"""
Botesdale Dental — static site generator.

This script assembles every page in /pages and /index.html from the shared
partials and the content defined in tools/content.py. It exists so that the
header, footer, meta tags and component markup stay identical across 35 pages.

    python3 tools/build.py

It writes plain, dependency-free HTML — the output is the deliverable and can
be edited by hand. Re-running the script OVERWRITES those files, so once you
start hand-editing pages, either stop using it or fold your edits back into
tools/content.py.
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content import SITE, NAV, PAGES, PAGE_ORDER, ROUTES   # noqa: E402


# =============================================================================
# Path helpers
# =============================================================================
def route(key):
    """Root-relative path for a page key."""
    if key not in ROUTES:
        raise KeyError("Unknown page key: %s" % key)
    return ROUTES[key]


def rel(target_key, depth):
    """Path to a page key from a document nested `depth` folders deep."""
    return ('../' * depth) + route(target_key)


def asset(path, depth):
    return ('../' * depth) + 'assets/' + path.lstrip('/')


def esc(s):
    return html.escape(s, quote=True)


# =============================================================================
# Shared fragments
# =============================================================================
ARC = ('<svg class="arc" viewBox="0 0 100 8" preserveAspectRatio="none" aria-hidden="true">'
       '<path d="M0,1 Q50,7 100,1" pathLength="100"/></svg>')

SMILE_DEFS = '''<svg class="svg-defs" aria-hidden="true" focusable="false">
  <defs>
    <clipPath id="smileClip" clipPathUnits="objectBoundingBox">
      <path d="M0,0.08 Q0.5,0.4 1,0.08 L1,1 L0,1 Z"/>
    </clipPath>
    <!-- The same smile, on the bottom edge of the dark hero panels. The control
         point sits past 1 so the curve reaches exactly full height at the
         centre and lifts to 0.955 at the sides — the panel keeps its depth
         where the copy sits and the arc only ever cuts into the corners. -->
    <clipPath id="heroArc" clipPathUnits="objectBoundingBox">
      <path d="M0,0 L1,0 L1,0.955 Q0.5,1.045 0,0.955 Z"/>
    </clipPath>
  </defs>
</svg>'''


def btn(label, href, variant='solid', extra=''):
    return ('<a class="btn btn--%s%s" href="%s">'
            '<span class="btn__fill"></span>'
            '<span class="btn__label">%s</span></a>'
            % (variant, (' ' + extra) if extra else '', href, esc(label)))


def arc_link(label, href, light=False):
    cls = 'arc-link arc-link--light' if light else 'arc-link'
    return '<a class="%s" href="%s"><span>%s</span>%s</a>' % (cls, href, esc(label), ARC)


# =============================================================================
# Header
# =============================================================================
def build_header(active, depth):
    links = []
    for item in NAV:
        is_active = active == item['key'] or active in item.get('children_keys', [])
        cls = 'nav__link is-active' if is_active else 'nav__link'
        anchor = '<a class="%s" href="%s"><span>%s</span>%s</a>' % (
            cls, rel(item['key'], depth), esc(item['label']), ARC)

        if item.get('children'):
            sub = []
            for child in item['children']:
                ccls = ' class="is-active"' if active == child['key'] else ''
                sub.append('<a href="%s"%s>%s</a>' % (rel(child['key'], depth), ccls, esc(child['label'])))
            links.append('<div class="nav__dd">%s<div class="nav__panel">%s</div></div>'
                         % (anchor, ''.join(sub)))
        else:
            links.append(anchor)

    # ---- mobile sheet -------------------------------------------------------
    sheet = []
    for i, item in enumerate(NAV):
        if item.get('children'):
            gid = 'menuGroup%d' % i
            subs = []
            for child in item['children']:
                ccls = ' class="is-active"' if active == child['key'] else ''
                subs.append('<a href="%s"%s>%s</a>' % (rel(child['key'], depth), ccls, esc(child['label'])))
            sheet.append(
                '<div class="menu__group">'
                '<button class="menu__toggle" type="button" aria-expanded="false" aria-controls="%s">'
                '<span>%s</span>'
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
                '<path d="M6 9l6 6 6-6"/></svg></button>'
                '<div class="menu__sub" id="%s">'
                '<a href="%s">%s overview</a>%s</div></div>'
                % (gid, esc(item['label']), gid, rel(item['key'], depth),
                   esc(item['label']), ''.join(subs)))
        else:
            sheet.append('<a class="menu__link" href="%s"><span>%s</span>%s</a>'
                         % (rel(item['key'], depth), esc(item['label']), ARC))

    return '''<header class="nav" data-nav-root>
  <div class="nav__inner">
    <a class="brand" href="{home}">Botesdale Dental<span class="brand__dot" aria-hidden="true"></span></a>
    <nav class="nav__links" aria-label="Primary">
      {links}
    </nav>
    <a class="nav__cta" href="{contact}"><span class="btn__label">Book a visit</span></a>
    <button class="nav__toggle" id="menuOpen" type="button" aria-expanded="false"
            aria-controls="mobileMenu" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<div class="menu" id="mobileMenu">
  <button class="menu__close" id="menuClose" type="button">Close</button>
  {sheet}
  <a class="menu__cta" href="{contact}">Book a visit</a>
  <div class="menu__contact">
    <a href="tel:{tel_href}">{tel}</a>
    <a href="mailto:{email}">{email}</a>
  </div>
</div>'''.format(
        home=rel('home', depth),
        contact=rel('contact', depth),
        links='\n      '.join(links),
        sheet='\n  '.join(sheet),
        tel=SITE['phone'], tel_href=SITE['phone_href'], email=SITE['email'])


# =============================================================================
# Footer
# =============================================================================
def build_footer(depth):
    def flink(key, label):
        return '<a class="footer__link" href="%s"><span>%s</span>%s</a>' % (
            rel(key, depth), esc(label), ARC)

    site_links = ''.join(flink(k, l) for k, l in [
        ('home', 'Home'), ('about', 'About us'), ('fees', 'Fees and membership'),
        ('referrals', 'Referrals'), ('cases', 'Case studies'), ('contact', 'Contact us')])

    treat_links = ''.join(flink(k, l) for k, l in [
        ('general', 'General dentistry'), ('cosmetic', 'Cosmetic dentistry'),
        ('preventative', 'Preventative dentistry'), ('missing', 'Missing teeth'),
        ('implant', 'Implant clinic'), ('implant-referrals', 'Implant referrals')])

    hours = ''.join('<div class="footer__hours"><span>%s</span><span>%s</span></div>' % (d, h)
                    for d, h in SITE['hours'])

    return '''<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">

      <div class="footer__col">
        <span class="label">Site</span>
        {site_links}
      </div>

      <div class="footer__col">
        <span class="label">Treatments</span>
        {treat_links}
      </div>

      <div class="footer__col">
        <span class="label">Opening hours</span>
        {hours}
      </div>

      <div class="footer__col">
        <span class="label">Get in touch</span>
        <address class="footer__address">
          Botesdale Dental Practice &amp; Implant Clinic<br>
          Holly Close, The Drift<br>
          Botesdale, Suffolk IP22 1DH
        </address>
        <a class="footer__strong" href="tel:{tel_href}"><span>{tel}</span>{arc}</a>
        <a class="footer__strong" href="mailto:{email}"><span>{email}</span>{arc}</a>
        <div class="footer__social">
          <a href="{facebook}" aria-label="Botesdale Dental on Facebook" rel="noopener">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
              <path d="M14 9h3V6h-3c-1.66 0-3 1.34-3 3v2H9v3h2v6h3v-6h2.5l.5-3H14V9z"/></svg>
          </a>
          <a href="{instagram}" aria-label="Botesdale Dental on Instagram" rel="noopener">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
              <rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="3.7"/>
              <circle cx="17.2" cy="6.8" r="0.6" fill="currentColor" stroke="none"/></svg>
          </a>
        </div>
      </div>

    </div>

    <div class="footer__bottom">
      <div class="footer__legal">
        <a href="{privacy}">Privacy Policy</a>
        <a href="{cookies}">Cookie Policy</a>
        <a href="{styleguide}">Style guide</a>
      </div>
      <div>&copy; <span data-year>2026</span> &middot; Botesdale Dental Practice &middot; Registered in England and Wales, company number 123456.</div>
    </div>
  </div>
</footer>

<button class="to-top" type="button" data-to-top aria-label="Back to top">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
    <path d="M12 19V5M5 12l7-7 7 7"/></svg>
</button>

<div class="cookie" id="cookieBanner" role="region" aria-label="Cookie notice">
  <div class="wrap cookie__inner">
    <p>We use a small number of essential cookies to make this site work. See our
      <a href="{cookies}">Cookie Policy</a> for details.</p>
    <div class="cookie__actions">
      <button class="btn btn--light btn--sm" type="button" data-cookie-choice="accepted">
        <span class="btn__fill"></span><span class="btn__label">Accept</span></button>
      <button class="btn btn--light btn--sm" type="button" data-cookie-choice="essential">
        <span class="btn__fill"></span><span class="btn__label">Essential only</span></button>
    </div>
  </div>
</div>

<div class="lightbox" id="lightbox" role="dialog" aria-label="Enlarged image">
  <button class="lightbox__close" type="button">Close</button>
  <img alt="">
</div>'''.format(
        site_links=site_links, treat_links=treat_links, hours=hours, arc=ARC,
        tel=SITE['phone'], tel_href=SITE['phone_href'], email=SITE['email'],
        facebook=SITE['facebook'], instagram=SITE['instagram'],
        privacy=rel('privacy', depth), cookies=rel('cookies', depth),
        styleguide=rel('styleguide', depth))


# =============================================================================
# Document shell
# =============================================================================
def document(page, body, depth):
    canonical = SITE['base_url'].rstrip('/') + '/' + route(page['key'])
    if canonical.endswith('/index.html'):
        canonical = canonical[:-len('index.html')]

    return '''<!DOCTYPE html>
<html lang="en-GB" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Botesdale Dental Practice &amp; Implant Clinic">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E1116">

<link rel="icon" href="{favicon}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

<link rel="stylesheet" href="{css}base.css">
<link rel="stylesheet" href="{css}layout.css">
<link rel="stylesheet" href="{css}components.css">
<link rel="stylesheet" href="{css}pages.css">
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>
{defs}

{header}

<main id="main">
{body}
</main>

{footer}

<script src="{js}nav.js" defer></script>
<script src="{js}ui.js" defer></script>
<script src="{js}forms.js" defer></script>
<script src="{js}main.js" defer></script>
</body>
</html>
'''.format(
        title=esc(page['title']),
        description=esc(page['description']),
        canonical=canonical,
        favicon=asset('images/brand/favicon.svg', depth),
        css=('../' * depth) + 'css/',
        js=('../' * depth) + 'js/',
        defs=SMILE_DEFS,
        header=build_header(page['key'], depth),
        body=body,
        footer=build_footer(depth))


# =============================================================================
# Build
# =============================================================================
def main():
    from content import render_body
    written = []
    for key in PAGE_ORDER:
        page = PAGES[key]
        path = route(key)
        depth = path.count('/')
        body = render_body(key, page, depth, helpers)
        out = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'w', encoding='utf-8') as fh:
            fh.write(document(page, body, depth))
        written.append(path)

    # sitemap.xml
    urls = []
    for key in PAGE_ORDER:
        if key == '404':
            continue
        loc = SITE['base_url'].rstrip('/') + '/' + route(key)
        if loc.endswith('/index.html'):
            loc = loc[:-len('index.html')]
        prio = '1.0' if key == 'home' else ('0.8' if depth_of(key) else '0.7')
        urls.append('  <url><loc>%s</loc><priority>%s</priority></url>' % (loc, prio))
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + '\n'.join(urls) + '\n</urlset>\n')

    print('Wrote %d pages + sitemap.xml' % len(written))
    for p in written:
        print('  ' + p)


def depth_of(key):
    return route(key).count('/')


# Bundle of helpers handed to the content module
class helpers:
    rel = staticmethod(rel)
    asset = staticmethod(asset)
    esc = staticmethod(esc)
    btn = staticmethod(btn)
    arc_link = staticmethod(arc_link)
    ARC = ARC


if __name__ == '__main__':
    main()
