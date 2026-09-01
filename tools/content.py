# -*- coding: utf-8 -*-
"""
Botesdale Dental — site content and page composition.

Everything a copywriter or the practice would want to change lives here:
site-wide details, the navigation tree, page titles and meta descriptions,
and the body content of each page expressed with the component builders
below. build.py wraps whatever this module returns in the shared shell.
"""

# =============================================================================
# SITE
# =============================================================================
SITE = {
    'name':       'Botesdale Dental Practice & Implant Clinic',
    'short':      'Botesdale Dental',
    'base_url':   'https://botesdaledental.co.uk',
    'phone':      '01379 897176',
    'phone_href': '+441379897176',
    'email':      'reception@botesdaledental.co.uk',
    'address': ['Botesdale Dental Practice & Implant Clinic',
                'Holly Close', 'The Drift', 'Botesdale', 'Suffolk IP22 1DH'],
    'facebook':  'https://www.facebook.com/botesdaledental',
    'instagram': 'https://www.instagram.com/botesdaledental',
    'hours': [('Monday', '9am–3pm'), ('Tuesday', '9am–3pm'), ('Wednesday', '9am–4pm'),
              ('Thursday', '9am–4pm'), ('Friday', '9am–3pm')],
    'company_no': '123456',
}

# =============================================================================
# ROUTES — page key → path from the site root
# =============================================================================
ROUTES = {
    'home':               'index.html',
    '404':                '404.html',
    'about':              'pages/about-us.html',
    'treatments':         'pages/treatments.html',

    'general':            'pages/general-dentistry.html',
    'root-canal':         'pages/root-canal-therapy.html',
    'extractions':        'pages/extractions.html',
    'emergency':          'pages/emergency-dental-treatment.html',
    'nervous':            'pages/nervous-patients.html',

    'cosmetic':           'pages/cosmetic-dentistry.html',
    'clear-aligner':      'pages/clear-aligner.html',
    'veneers':            'pages/veneers.html',
    'crowns':             'pages/crowns.html',
    'bridges':            'pages/bridges.html',
    'whitening':          'pages/teeth-whitening.html',
    'gum-reshaping':      'pages/gum-reshaping.html',

    'preventative':       'pages/preventative-dentistry.html',
    'check-up':           'pages/check-up.html',
    'hygiene':            'pages/dental-hygiene.html',
    'sensitive':          'pages/sensitive-teeth.html',

    'missing':            'pages/missing-teeth.html',

    'implant':            'pages/implant-clinic.html',
    'implant-referrals':  'pages/implant-referrals.html',

    'referrals':          'pages/referrals.html',
    'fees':               'pages/fees-and-membership.html',

    'cases':              'pages/case-studies.html',
    'case-worn':          'pages/case-treating-worn-dentition.html',
    'case-missing':       'pages/case-replacement-of-missing-teeth.html',
    'case-newdenture':    'pages/case-new-upper-denture.html',
    'case-loose':         'pages/case-loose-upper-denture.html',
    'case-sameday':       'pages/case-same-day-teeth.html',

    'contact':            'pages/contact-us.html',
    'privacy':            'pages/privacy-policy.html',
    'cookies':            'pages/cookie-policy.html',
    'styleguide':         'pages/style-guide.html',
}

# =============================================================================
# NAV — mirrors the client sitemap exactly
# =============================================================================
NAV = [
    {'key': 'about',      'label': 'About us'},
    {'key': 'treatments', 'label': 'Treatments',
     'children': [
         {'key': 'general',      'label': 'General dentistry'},
         {'key': 'cosmetic',     'label': 'Cosmetic dentistry'},
         {'key': 'preventative', 'label': 'Preventative dentistry'},
         {'key': 'missing',      'label': 'Missing teeth'},
     ],
     'children_keys': ['general', 'root-canal', 'extractions', 'emergency', 'nervous',
                       'cosmetic', 'clear-aligner', 'veneers', 'crowns', 'bridges',
                       'whitening', 'gum-reshaping',
                       'preventative', 'check-up', 'hygiene', 'sensitive', 'missing']},
    {'key': 'implant',    'label': 'Implant clinic',
     'children': [
         {'key': 'implant',           'label': 'Implant clinic'},
         {'key': 'implant-referrals', 'label': 'Implant referrals'},
     ],
     'children_keys': ['implant-referrals']},
    {'key': 'referrals',  'label': 'Referrals'},
    {'key': 'fees',       'label': 'Fees'},
    {'key': 'cases',      'label': 'Case studies',
     'children_keys': ['case-worn', 'case-missing', 'case-newdenture',
                       'case-loose', 'case-sameday']},
    {'key': 'contact',    'label': 'Contact'},
]

# Sibling groups used by the contextual rail and the mobile group expansion
GROUPS = {
    'general':      ('General dentistry', ['general', 'root-canal', 'extractions', 'emergency', 'nervous']),
    'cosmetic':     ('Cosmetic dentistry', ['cosmetic', 'clear-aligner', 'veneers', 'crowns',
                                            'bridges', 'whitening', 'gum-reshaping']),
    'preventative': ('Preventative dentistry', ['preventative', 'check-up', 'hygiene', 'sensitive']),
    'cases':        ('Case studies', ['case-worn', 'case-missing', 'case-newdenture',
                                      'case-loose', 'case-sameday']),
}

LABELS = {
    'home': 'Home', 'about': 'About us', 'treatments': 'Treatments',
    'general': 'General dentistry', 'root-canal': 'Root canal therapy',
    'extractions': 'Extractions', 'emergency': 'Emergency dental treatment',
    'nervous': 'Nervous patients', 'cosmetic': 'Cosmetic dentistry',
    'clear-aligner': 'Clear aligner', 'veneers': 'Veneers', 'crowns': 'Crowns',
    'bridges': 'Bridges', 'whitening': 'Teeth whitening', 'gum-reshaping': 'Gum reshaping',
    'preventative': 'Preventative dentistry', 'check-up': 'Check up',
    'hygiene': 'Dental hygiene', 'sensitive': 'Sensitive teeth',
    'missing': 'Missing teeth', 'implant': 'Implant clinic',
    'implant-referrals': 'Implant referrals', 'referrals': 'Referrals',
    'fees': 'Fees and membership', 'cases': 'Case studies',
    'case-worn': 'Treating worn dentition with composite bonding',
    'case-missing': 'Replacement of missing teeth',
    'case-newdenture': 'New upper denture',
    'case-loose': 'Loose upper denture',
    'case-sameday': 'Same day teeth',
    'contact': 'Contact us', 'privacy': 'Privacy Policy', 'cookies': 'Cookie Policy',
    'styleguide': 'Style guide', '404': 'Page not found',
}


# =============================================================================
# COMPONENT BUILDERS
# Each returns a string of HTML. They are deliberately small and composable —
# a page is a list of these joined together.
# =============================================================================
def _trim(text, n):
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(' ', 1)[0].rstrip(' ,.;:')
    return cut + '…'


def _e(s):
    import html
    return html.escape(s, quote=True)


ARC = ('<svg class="arc" viewBox="0 0 100 8" preserveAspectRatio="none" aria-hidden="true">'
       '<path d="M0,1 Q50,7 100,1" pathLength="100"/></svg>')


def c_btn(label, href, variant='solid'):
    return ('<a class="btn btn--%s" href="%s"><span class="btn__fill"></span>'
            '<span class="btn__label">%s</span></a>' % (variant, href, _e(label)))


def c_arc_link(label, href, light=False):
    cls = 'arc-link arc-link--light' if light else 'arc-link'
    return '<a class="%s" href="%s"><span>%s</span>%s</a>' % (cls, href, _e(label), ARC)


def c_ph(label='', cls=''):
    """Grey image placeholder. Swap the whole element for an <img> when the
    practice's photography is ready — the parent sets the aspect ratio."""
    inner = '<span class="ph__label">%s</span>' % _e(label) if label else ''
    return '<div class="ph%s" role="img" aria-label="%s">%s</div>' % (
        (' ' + cls) if cls else '', _e(label or 'Image placeholder'), inner)


def c_crumbs(H, depth, trail, current):
    """trail: list of page keys leading to the current page."""
    parts = ['<a href="%s">Home</a>' % H.rel('home', depth)]
    for key in trail:
        parts.append('<a href="%s">%s</a>' % (H.rel(key, depth), _e(LABELS[key])))
    parts.append('<span aria-current="page">%s</span>' % _e(current))
    sep = '<span class="crumbs__sep" aria-hidden="true">/</span>'
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % sep.join(parts)


def c_hero(H, depth, eyebrow, heading, sub, image, actions=''):
    return '''<section class="hero">
  <!-- Background photograph goes here:
       <img class="hero__media" src="assets/images/heroes/home.jpg" alt=""> -->
  <div class="hero__scrim"></div>
  <span class="ph-note" aria-hidden="true">Hero photograph</span>
  <div class="hero__inner wrap">
    <span class="label">{eyebrow}</span>
    <h1 class="display">{heading}</h1>
    <p class="hero__sub">{sub}</p>
    {actions}
  </div>
</section>'''.format(eyebrow=_e(eyebrow), heading=heading, sub=_e(sub),
                     actions=('<div class="hero__actions btn-row">%s</div>' % actions) if actions else '')


def c_page_head(H, depth, eyebrow, heading, sub='', image=None, crumbs='', short=False):
    if eyebrow.strip().lower() == heading.strip().lower():
        eyebrow = ''
    return '''<section class="page-head{short}">
  <!-- Background photograph goes here:
       <img class="page-head__media" src="../assets/images/heroes/NAME.jpg" alt=""> -->
  <div class="page-head__scrim"></div>
  <span class="ph-note" aria-hidden="true">Header photograph</span>
  <div class="page-head__inner wrap">
    {crumbs}
    {eyebrow}
    <h1>{heading}</h1>
    {sub}
  </div>
</section>'''.format(short=' page-head--short' if short else '', crumbs=crumbs,
                     eyebrow=('<span class="label">%s</span>' % _e(eyebrow)) if eyebrow else '',
                     heading=_e(heading),
                     sub=('<p>%s</p>' % _e(sub)) if sub else '')


def c_ed(H, depth, eyebrow, heading, paras, link=None, image=None, rev=False,
         warm=False, alt='', media_wide=False):
    wrap_cls = 'ed'
    if rev:
        wrap_cls += ' ed--rev'
    if media_wide:
        wrap_cls += ' ed--media-wide'
    body = ''.join('<p>%s</p>' % p for p in paras)
    link_html = c_arc_link(link[0], link[1]) if link else ''
    return '''<section class="{wrap_cls}" data-reveal>
  <div class="ed__media">{ph}</div>
  <div class="ed__text">
    <span class="label">{eyebrow}</span>
    <h2>{heading}</h2>
    {body}
    {link}
  </div>
</section>'''.format(wrap_cls=wrap_cls, ph=c_ph(alt or heading),
                     eyebrow=_e(eyebrow), heading=_e(heading), body=body, link=link_html)


def c_strip(H, depth, eyebrow, heading, items, cols=3):
    """items: list of dicts {key|href, label, title, text, alt}"""
    tiles = []
    for i, it in enumerate(items):
        href = it.get('href') or H.rel(it['key'], depth)
        tiles.append('''<a class="strip__item" href="{href}" data-reveal data-reveal-delay="{d}">
        <div class="strip__media">{ph}</div>
        <div class="strip__cap">
          <span class="label">{label}</span>
          <h3>{title}</h3>
          <p>{text}</p>
          <span class="arc-link"><span>Read more</span>{arc}</span>
        </div>
      </a>'''.format(href=href, d=min(i, 3), ph=c_ph(it.get('alt') or it['title']),
                     label=_e(it.get('label', '')), title=_e(it['title']),
                     text=_e(it['text']), arc=ARC))

    head = ''
    if heading:
        head = ('<div class="strip__head"><span class="label">%s</span><h2>%s</h2></div>'
                % (_e(eyebrow), _e(heading)))
    return '''<section class="strip">
  <div class="wrap">
    {head}
    <div class="strip__row strip__row--{cols}">
      {tiles}
    </div>
  </div>
</section>'''.format(head=head, cols=cols, tiles='\n      '.join(tiles))


def c_cards(H, depth, items, cols=3):
    out = []
    for it in items:
        href = it.get('href') or H.rel(it['key'], depth)
        out.append('''<a class="card" href="{href}" data-reveal>
      <div class="card__media">{ph}</div>
      <div class="card__body">
        <span class="label">{label}</span>
        <h3>{title}</h3>
        <p>{text}</p>
        <span class="arc-link"><span>Read more</span>{arc}</span>
      </div>
    </a>'''.format(href=href, ph=c_ph(it.get('alt') or it['title']),
                   label=_e(it.get('label', '')), title=_e(it['title']),
                   text=_e(it['text']), arc=ARC))
    return '<div class="cols-%d">%s</div>' % (cols, '\n    '.join(out))


def c_process(H, depth, eyebrow, heading, rows, top_line=True):
    body = []
    for i, (title, text) in enumerate(rows, 1):
        body.append('''<div class="p-row" data-reveal>
      <div class="p-row__num">{n:02d}</div>
      <div><h3>{title}</h3><p>{text}</p></div>
    </div>'''.format(n=i, title=_e(title), text=text))
    return '''<section class="process{cls}">
  <div class="wrap">
    <div class="process__head">
      <span class="label">{eyebrow}</span>
      <h2>{heading}</h2>
    </div>
    {body}
  </div>
</section>'''.format(cls='' if top_line else ' section--no-line', eyebrow=_e(eyebrow),
                     heading=_e(heading), body='\n    '.join(body))


def c_statement(H, depth, eyebrow, heading, para, facts=None, link=None):
    facts_html = ''
    if facts:
        items = ''.join('<div class="fact"><div class="fact__num">%s</div>'
                        '<div class="fact__cap">%s</div></div>' % (n, _e(c))
                        for n, c in facts)
        facts_html = '<div class="facts">%s</div>' % items
    link_html = ('<div class="u-mt-8">%s</div>' % c_arc_link(link[0], link[1], light=True)) if link else ''
    return '''<section class="statement" data-reveal>
  <div class="wrap">
    <span class="label">{eyebrow}</span>
    <h2>{heading}</h2>
    <p>{para}</p>
    {facts}
    {link}
  </div>
</section>'''.format(eyebrow=_e(eyebrow), heading=_e(heading), para=_e(para),
                     facts=facts_html, link=link_html)


def c_quote(quotes):
    """quotes: list of (text, name). Renders a carousel when there is more than one."""
    if len(quotes) == 1:
        t, n = quotes[0]
        return ('<section class="quote"><div class="wrap">'
                '<blockquote>&ldquo;%s&rdquo;</blockquote>'
                '<div class="quote__name">%s</div></div></section>' % (_e(t), _e(n)))
    slides = ''.join(
        '<div class="carousel__slide%s"><blockquote>&ldquo;%s&rdquo;</blockquote>'
        '<div class="quote__name">%s</div></div>'
        % (' is-active' if i == 0 else '', _e(t), _e(n))
        for i, (t, n) in enumerate(quotes))
    return '''<section class="quote">
  <div class="wrap">
    <div class="carousel" data-carousel data-carousel-interval="8000">
      <div class="carousel__track">{slides}</div>
      <div class="carousel__nav">
        <button class="carousel__btn" type="button" data-carousel-prev aria-label="Previous review">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>
        </button>
        <div class="carousel__dots"></div>
        <button class="carousel__btn" type="button" data-carousel-next aria-label="Next review">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>
        </button>
      </div>
    </div>
  </div>
</section>'''.format(slides=slides)


def c_accordion(items, single=True, idbase='acc'):
    rows = []
    for i, (q, a) in enumerate(items, 1):
        pid = '%s-panel-%d' % (idbase, i)
        rows.append('''<div class="accordion__item">
      <h3><button class="accordion__btn" type="button" aria-expanded="false" aria-controls="{pid}">
        <span>{q}</span><span class="accordion__icon" aria-hidden="true"></span>
      </button></h3>
      <div class="accordion__panel" id="{pid}">
        <div class="accordion__panel-inner">{a}</div>
      </div>
    </div>'''.format(pid=pid, q=_e(q), a=a))
    return '<div class="accordion"%s>%s</div>' % (' data-single' if single else '',
                                                  '\n    '.join(rows))


def c_rail(H, depth, current, group_key):
    title, keys = GROUPS[group_key]
    links = []
    for k in keys:
        cls = ' class="is-active"' if k == current else ''
        links.append('<a href="%s"%s>%s</a>' % (H.rel(k, depth), cls, _e(LABELS[k])))
    return '''<aside class="rail">
  <span class="label">{title}</span>
  <nav class="rail__list" aria-label="{title}">{links}</nav>
</aside>'''.format(title=_e(title), links=''.join(links))


def c_specs(rows):
    body = ''.join('<div class="spec"><span class="spec__k">%s</span>'
                   '<span class="spec__v">%s</span></div>' % (_e(k), v) for k, v in rows)
    return '<div class="specs">%s</div>' % body


def c_cta(H, depth, heading, para='', primary=('Book an appointment', 'contact'),
          secondary=None, dark=False):
    buttons = [c_btn(primary[0], H.rel(primary[1], depth),
                     'light' if dark else 'solid')]
    if secondary:
        buttons.append(c_btn(secondary[0], H.rel(secondary[1], depth),
                             'light' if dark else 'outline'))
    return '''<section class="cta{dark}">
  <div class="wrap">
    <h2>{heading}</h2>
    {para}
    <div class="btn-row">{buttons}</div>
  </div>
</section>'''.format(dark=' cta--dark' if dark else '', heading=_e(heading),
                     para=('<p>%s</p>' % _e(para)) if para else '',
                     buttons=''.join(buttons))


def c_pager(H, depth, prev=None, next_=None):
    left = ''
    right = ''
    if prev:
        left = ('<a class="pager__item pager__item--prev" href="%s">'
                '<span class="label">Previous</span><span class="pager__title">%s</span></a>'
                % (H.rel(prev, depth), _e(LABELS[prev])))
    if next_:
        right = ('<a class="pager__item pager__item--next" href="%s">'
                 '<span class="label">Next</span><span class="pager__title">%s</span></a>'
                 % (H.rel(next_, depth), _e(LABELS[next_])))
    return '<nav class="pager" aria-label="Case studies">%s%s</nav>' % (left, right)


def c_gallery(H, depth, shots):
    """shots: list of (image, tag, alt) — rendered as placeholders for now."""
    out = []
    for img, tag, alt in shots:
        tag_html = '<span class="shot__tag">%s</span>' % _e(tag) if tag else ''
        out.append('<figure class="shot">%s%s</figure>' % (c_ph(alt), tag_html))
    return '<div class="gallery">%s</div>' % ''.join(out)


def c_section(inner, cls='', wrap=True):
    body = '<div class="wrap">%s</div>' % inner if wrap else inner
    return '<section class="section%s">%s</section>' % ((' ' + cls) if cls else '', body)


# =============================================================================
# PAGE META — <title> and meta description for every page
# =============================================================================
def _p(key, title, description):
    return {'key': key, 'title': title, 'description': description}


PAGES = {
 'home': _p('home', 'Botesdale Dental Practice & Implant Clinic | Dentist in Botesdale, Suffolk',
            'A modern, patient-centred dental practice in Botesdale, Suffolk. Family dentistry, '
            'cosmetic treatment and advanced dental implants, all under one roof.'),
 'about': _p('about', 'About us | Botesdale Dental Practice & Implant Clinic',
             'Meet Dr Martin Sulo and the team at Botesdale Dental Practice & Implant Clinic — a '
             'family-run practice in a purpose-built home in the heart of Botesdale.'),
 'treatments': _p('treatments', 'Treatments | Botesdale Dental Practice & Implant Clinic',
                  'General, cosmetic and preventative dentistry plus solutions for missing teeth, '
                  'all delivered at our Botesdale practice in Suffolk.'),

 'general': _p('general', 'General dentistry | Botesdale Dental Practice',
               'Your trusted local family dental practice for all kinds of general dentistry — '
               'root canal therapy, extractions, emergency care and support for nervous patients.'),
 'root-canal': _p('root-canal', 'Root canal therapy | Botesdale Dental Practice',
                  'Root canal treatment at our Botesdale practice: what it involves, when it is '
                  'needed and what to expect afterwards.'),
 'extractions': _p('extractions', 'Tooth extractions | Botesdale Dental Practice',
                   'Gentle tooth extraction in Botesdale, Suffolk — including wisdom teeth, with '
                   'clear aftercare and replacement options discussed in advance.'),
 'emergency': _p('emergency', 'Emergency dental treatment | Botesdale Dental Practice',
                 'Chipped, broken or knocked-out tooth? We do our best to provide same-day '
                 'emergency dental appointments for our patients in Botesdale.'),
 'nervous': _p('nervous', 'Nervous patients | Botesdale Dental Practice',
               'Anxious about the dentist? Our team takes the time to make treatment calm, '
               'unhurried and completely under your control.'),

 'cosmetic': _p('cosmetic', 'Cosmetic dentistry | Botesdale Dental Practice',
                'Treatments that enhance, align, whiten and tone your teeth — veneers, crowns, '
                'bridges, whitening, clear aligners and gum reshaping in Botesdale.'),
 'clear-aligner': _p('clear-aligner', 'Clear aligners | Botesdale Dental Practice',
                     'Invisible orthodontics — straighter teeth without metal braces, planned '
                     'digitally at our Botesdale practice.'),
 'veneers': _p('veneers', 'Porcelain veneers | Botesdale Dental Practice',
               'Veneers for stained, chipped or misaligned front teeth, designed and fitted at '
               'our Botesdale practice in Suffolk.'),
 'crowns': _p('crowns', 'Dental crowns | Botesdale Dental Practice',
              'Crowns restore teeth that are broken, weakened by decay or hold a very large '
              'filling — including same-day crowns crafted on site.'),
 'bridges': _p('bridges', 'Dental bridges | Botesdale Dental Practice',
               'A fixed, natural-looking way to replace one or more missing teeth without '
               'surgery, made with our UK and European laboratory partners.'),
 'whitening': _p('whitening', 'Teeth whitening | Botesdale Dental Practice',
                 'Professional, dentist-supervised teeth whitening with custom-made trays — '
                 'safe, gradual and tailored to your teeth.'),
 'gum-reshaping': _p('gum-reshaping', 'Gum reshaping | Botesdale Dental Practice',
                     'Periodontics focused on the health and treatment of gums and bone, '
                     'correcting and preventing damage and evening out a gummy smile.'),

 'preventative': _p('preventative', 'Preventative dentistry | Botesdale Dental Practice',
                    'Routine dental appointments are essential to maintain good oral health — '
                    'check-ups, hygiene visits and help with sensitive teeth.'),
 'check-up': _p('check-up', 'Dental check up | Botesdale Dental Practice',
                'A standard dental check-up carried out by an experienced, qualified dentist to '
                'spot any problems before they become serious.'),
 'hygiene': _p('hygiene', 'Dental hygiene | Botesdale Dental Practice',
               'Hygiene treatment delivered by a specially trained professional to remove '
               'hard-to-reach plaque and protect your gums.'),
 'sensitive': _p('sensitive', 'Sensitive teeth | Botesdale Dental Practice',
                 'Shooting pain when you eat or drink something hot or cold? We find the cause '
                 'of tooth sensitivity and treat it properly.'),

 'missing': _p('missing', 'Missing teeth | Botesdale Dental Practice',
               'Crowns, bridges, dentures and dental implants — the options for replacing '
               'missing teeth, explained clearly.'),

 'implant': _p('implant', 'Implant clinic | Botesdale Dental Practice & Implant Clinic',
               'Dental implants offer a proven, long-lasting solution for bringing back your '
               'smile and restoring your ability to bite and chew comfortably.'),
 'implant-referrals': _p('implant-referrals', 'Implant referrals | Botesdale Dental Practice',
                         'Patient self-referrals and dental professional referrals for implant '
                         'assessment and treatment at our Botesdale implant clinic.'),

 'referrals': _p('referrals', 'CBCT & OPG referrals | Botesdale Dental Practice',
                 'A reliable and efficient CBCT and OPG referral service for professional '
                 'colleagues, with fast turnaround and clear, precise scans.'),
 'fees': _p('fees', 'Fees and membership | Botesdale Dental Practice',
            'Our Plan membership from £19.95 per month, private fee guide, finance options and '
            'everything included in your dental membership.'),

 'cases': _p('cases', 'Case studies | Botesdale Dental Practice',
             'Real patients, real results. Case studies published with the consent and kind '
             'agreement of our patients.'),
 'case-worn': _p('case-worn', 'Treating worn dentition with composite bonding | Case study',
                 'A minimally invasive composite bonding case restoring worn, cracked front '
                 'teeth using digital planning.'),
 'case-missing': _p('case-missing', 'Replacement of missing teeth | Case study',
                    'A self-referred patient unhappy with previous "patch up work" on the front '
                    'teeth — treated with eMax veneers, crowns and a partial denture.'),
 'case-newdenture': _p('case-newdenture', 'New upper denture | Case study',
                       'An 82-year-old patient wanting the best possible denture without the use '
                       'of dental implants.'),
 'case-loose': _p('case-loose', 'Loose upper denture | Case study',
                  'Four dental implants supporting a screw-retained, non-removable set of ten '
                  'new teeth with no palatal coverage.'),
 'case-sameday': _p('case-sameday', 'Same day teeth | Case study',
                    'Six remaining lower teeth and a failing bridge — treated with an '
                    'implant-supported same day solution.'),

 'contact': _p('contact', 'Contact us | Botesdale Dental Practice & Implant Clinic',
               'Register as a new patient or get in touch with Botesdale Dental Practice & '
               'Implant Clinic, Holly Close, The Drift, Botesdale, Suffolk IP22 1DH.'),
 'privacy': _p('privacy', 'Privacy Policy | Botesdale Dental Practice',
               'How Botesdale Dental Practice & Implant Clinic collects, uses and protects your '
               'personal information.'),
 'cookies': _p('cookies', 'Cookie Policy | Botesdale Dental Practice',
               'The cookies this website uses, what each one is for and how long it stays on '
               'your device.'),
 'styleguide': _p('styleguide', 'Style guide | Botesdale Dental design system',
                  'Living reference for the Botesdale Dental design system — colour, type, '
                  'spacing and every reusable component.'),
 '404': _p('404', 'Page not found | Botesdale Dental Practice',
           'Sorry, we could not find that page.'),
}

PAGE_ORDER = ['home', 'about', 'treatments',
              'general', 'root-canal', 'extractions', 'emergency', 'nervous',
              'cosmetic', 'clear-aligner', 'veneers', 'crowns', 'bridges',
              'whitening', 'gum-reshaping',
              'preventative', 'check-up', 'hygiene', 'sensitive',
              'missing', 'implant', 'implant-referrals',
              'referrals', 'fees',
              'cases', 'case-worn', 'case-missing', 'case-newdenture',
              'case-loose', 'case-sameday',
              'contact', 'privacy', 'cookies', 'styleguide', '404']


# =============================================================================
# LEAF TREATMENT PAGES
# One entry per child box in the sitemap. All rendered by render_leaf().
# =============================================================================
LEAF = {
 'root-canal': {
   'group': 'general', 'parent': 'general',
   'hero': 'images/heroes/general.jpg',
   'sub': 'Saving a tooth that would otherwise be lost.',
   'lead': 'Root canal treatment is available at the practice. Following an initial assessment, '
           'and depending on the complexity of the case, it may be in the patient’s best '
           'interest to be referred to a specialist endodontist.',
   'paras': [
     'A root canal is needed when the soft tissue inside a tooth — the pulp — becomes infected '
     'or inflamed, usually through deep decay, a crack, or repeated treatment on the same tooth. '
     'Left alone, that infection spreads into the bone around the root and the tooth is normally '
     'lost.',
     'The treatment removes the infected tissue, cleans and shapes the canals inside the root, '
     'and seals them. The tooth stays where it is. In most cases it is then restored with a crown '
     'so that it can take the full force of biting again.'],
   'image': 'images/cards/root-canal-therapy.jpg',
   'process': [
     ('Assessment and X-rays', 'We take radiographs to see the shape of the roots and the extent '
      'of the infection, and explain what we find before anything is agreed.'),
     ('Local anaesthetic', 'The tooth and the area around it are fully numbed. Modern root canal '
      'treatment should feel no different to having a filling.'),
     ('Cleaning and shaping', 'The canals are cleaned, disinfected and shaped. Complex cases may '
      'be spread over more than one visit.'),
     ('Filling and sealing', 'The canals are sealed to stop bacteria getting back in, and the '
      'tooth is closed with a permanent restoration.'),
     ('Protecting the tooth', 'A root-treated back tooth is usually crowned. A crown holds the '
      'remaining tooth structure together and greatly improves its long-term prospects.')],
   'faqs': [
     ('Does root canal treatment hurt?',
      '<p>The treatment itself is carried out under local anaesthetic and should feel much like '
      'having a filling. Most of the pain people associate with root canals comes from the '
      'infection beforehand — which the treatment relieves.</p>'),
     ('How long does the tooth last afterwards?',
      '<p>A well-restored root-treated tooth can last many years. The main risk is fracture, '
      'which is why we usually recommend a crown on back teeth.</p>'),
     ('What if the case is complicated?',
      '<p>Some roots are unusually curved, calcified or have been treated before. Where a case '
      'would be better handled under a microscope, we refer you to a specialist endodontist and '
      'stay involved throughout.</p>')],
 },

 'extractions': {
   'group': 'general', 'parent': 'general',
   'hero': 'images/heroes/general.jpg',
   'sub': 'When a tooth cannot be saved, removing it properly matters.',
   'lead': 'In cases of advanced gum disease and tooth decay, teeth may need to be extracted. '
           'Some patients may also develop impacted wisdom teeth, which can cause intense pain.',
   'paras': [
     'Taking a tooth out is always the last option, not the first. Where a tooth can be restored '
     'we will tell you so, and what that would involve. Where it genuinely cannot — because the '
     'decay reaches too far below the gum, the root is fractured, or the supporting bone has '
     'been lost to gum disease — leaving it in place usually causes more problems than removing '
     'it.',
     'We will always talk through what happens next before the tooth comes out, so you know '
     'whether the gap needs filling and what the options are.'],
   'image': 'images/cards/extractions.jpg',
   'process': [
     ('Assessment', 'X-rays show the root shape and its relationship to the nerve and sinus. We '
      'discuss whether the tooth can be saved.'),
     ('Numbing', 'The area is fully anaesthetised. You should feel pressure, but not pain.'),
     ('Removal', 'Straightforward extractions take a few minutes. Surgical extractions — often '
      'wisdom teeth — take longer and may need a stitch.'),
     ('Aftercare', 'You go home with clear written instructions: what to eat, how to keep the '
      'socket clean and what to do if anything worries you.'),
     ('Replacing the tooth', 'If the gap is visible or affects your bite, we will have already '
      'discussed a bridge, denture or implant so nothing comes as a surprise.')],
   'faqs': [
     ('How long does it take to heal?',
      '<p>The socket closes over within a week or two and bone fills in over the following '
      'months. Most people are back to normal within a couple of days.</p>'),
     ('Do I have to replace the tooth?',
      '<p>Not always. A back molar with a healthy tooth behind it may not need replacing. Where '
      'a gap would affect your bite, appearance or the neighbouring teeth, we will explain the '
      '<a class="link-inline" href="missing-teeth.html">replacement options</a>.</p>'),
     ('What about wisdom teeth?',
      '<p>Wisdom teeth only need removing if they are causing trouble — repeated infection, '
      'decay, or damage to the tooth in front. We assess each one individually.</p>')],
 },

 'emergency': {
   'group': 'general', 'parent': 'general',
   'hero': 'images/heroes/general.jpg',
   'sub': 'We do our best to see our regular patients the same day.',
   'lead': 'If you have chipped or broken a tooth as a result of an accident or injury, it is '
           'very important that you see a dentist as soon as possible. The same goes for one or '
           'more knocked-out teeth.',
   'paras': [
     'Dental pain rarely improves on its own, and an injured tooth is often easier to save in '
     'the first hours than the following week. Call the practice as early in the day as you can '
     'and we will do our best to fit you in.',
     'We do our very best to provide same-day emergency services for all of our regular '
     'patients, and will also try to accommodate others where we can. Members of Our Plan pay no '
     'emergency access fee and have worldwide dental injury and emergency cover.'],
   'image': 'images/cards/emergency-dental-treatment.jpg',
   'process': [
     ('Call us first', 'Phone <a class="link-inline" href="tel:+441379897176">01379 897176</a> '
      'rather than emailing. We can often give advice over the phone that helps straight away.'),
     ('Knocked-out adult tooth', 'Hold it by the crown, not the root. If it is clean, try to put '
      'it back in the socket and bite gently on a clean cloth. If not, keep it in milk and come '
      'straight in.'),
     ('Broken or chipped tooth', 'Keep any fragments. Rinse with warm salty water and avoid '
      'chewing on that side until you have been seen.'),
     ('Swelling', 'Facial swelling that is spreading, or that affects your eye, breathing or '
      'swallowing, needs urgent medical attention — go to A&amp;E.'),
     ('Out of hours', 'When the practice is closed, NHS 111 can direct you to the nearest '
      'urgent dental service.')],
   'faqs': [
     ('I am not registered with you. Can you still see me?',
      '<p>We prioritise our own patients, but we will always try to help. Call the practice and '
      'we will tell you honestly what we can do that day.</p>'),
     ('Is there an emergency fee?',
      '<p>Members of Our Plan pay a £0 emergency access fee. For everyone else there is an '
      'assessment fee, with any treatment quoted before it is carried out. See '
      '<a class="link-inline" href="fees-and-membership.html">fees and membership</a>.</p>')],
 },

 'nervous': {
   'group': 'general', 'parent': 'general',
   'hero': 'images/heroes/general.jpg',
   'sub': 'You are in control of the appointment, at every step.',
   'lead': 'We understand that you may not like coming to the dentist. This can lead to your '
           'teeth becoming decayed and gums diseased, leading to pain, tooth loss or even worse. '
           'Don’t worry — you’re not alone.',
   'paras': [
     'Dental anxiety is common and it is nothing to be embarrassed about. Quite often it comes '
     'from a bad experience years ago, or from feeling that things were happening without being '
     'explained. Both of those are avoidable.',
     'Tell us before you arrive. We will book a longer appointment, take things at your pace, '
     'explain each step before it happens and stop the moment you ask. For many nervous patients '
     'the first visit is nothing more than a conversation and a look — no instruments, no '
     'treatment, no pressure.'],
   'image': 'images/cards/nervous-patients.jpg',
   'process': [
     ('Tell us in advance', 'Mention it when you book. It changes how we plan the appointment, '
      'not how we treat you.'),
     ('A first visit with no treatment', 'Come in, sit down, meet the team and talk. Nothing '
      'else has to happen.'),
     ('Agree a stop signal', 'A raised hand stops everything, immediately. Knowing you can stop '
      'is often what makes it possible to continue.'),
     ('Small steps', 'We break treatment into short, manageable appointments rather than one '
      'long session.'),
     ('Build from there', 'Most anxious patients find that once the first two or three visits '
      'have gone well, the anxiety fades considerably.')],
   'faqs': [
     ('Will you judge me for how long it has been?',
      '<p>No. We see people who have avoided the dentist for years, and the reaction is always '
      'the same: let us have a look and work out a plan together.</p>'),
     ('Can I bring someone with me?',
      '<p>Yes. You are very welcome to bring a friend or family member into the surgery with '
      'you.</p>')],
 },

 'clear-aligner': {
   'group': 'cosmetic', 'parent': 'cosmetic',
   'hero': 'images/heroes/cosmetic.jpg',
   'sub': 'Straighter teeth without metal braces.',
   'lead': 'Invisible orthodontics is a solution to having straighter teeth without having to '
           'wear metal braces.',
   'paras': [
     'Clear aligners are a series of thin, transparent trays made to fit your teeth precisely. '
     'Each one moves the teeth a fraction further than the last. You wear them for most of the '
     'day and take them out to eat, drink and clean your teeth.',
     'Treatment starts with a digital scan and a plan you can see before you commit — including '
     'a simulation of the expected finishing position. Not every case suits aligners, and we '
     'will tell you honestly if fixed braces or a different approach would give a better '
     'result.'],
   'image': 'images/cards/clear-aligners.jpg',
   'process': [
     ('Consultation', 'We assess the position of your teeth, your bite and the health of the '
      'gums. Aligners only work on a healthy foundation.'),
     ('Digital scan and plan', 'A scan replaces the old impression trays. You see the projected '
      'result and the number of aligners before starting.'),
     ('Wearing the aligners', 'Typically 20–22 hours a day, changing to the next tray every one '
      'to two weeks.'),
     ('Reviews', 'Short check appointments make sure the teeth are tracking to plan.'),
     ('Retention', 'Teeth drift for life. A retainer at the end is not optional — it is what '
      'protects the result.')],
   'faqs': [
     ('How long does treatment take?',
      '<p>Mild crowding can be corrected in a few months. More complex cases run to a year or '
      'more. You will be given a realistic estimate at your consultation.</p>'),
     ('Will anyone notice I am wearing them?',
      '<p>They are far less visible than fixed braces, though close up they can be seen. Small '
      'tooth-coloured attachments are sometimes bonded to the teeth to help specific '
      'movements.</p>')],
 },

 'veneers': {
   'group': 'cosmetic', 'parent': 'cosmetic',
   'hero': 'images/heroes/cosmetic.jpg',
   'sub': 'A thin porcelain facing, bonded to the front of the tooth.',
   'lead': 'Are your teeth stained, chipped, or not aligned on top of each other? Veneers are an '
           'option to consider.',
   'paras': [
     'A veneer is a very thin layer of porcelain bonded to the front surface of a tooth. It '
     'changes the colour, shape and alignment of what you see, while leaving most of the natural '
     'tooth intact.',
     'Veneers involve special techniques, equipment and a high level of skill from the dental '
     'team. We work with certified technicians in the UK and Europe who specialise in this kind '
     'of work, and we plan the result with you before any tooth is prepared.'],
   'image': 'images/cards/veneers.jpg',
   'process': [
     ('Smile assessment', 'We photograph and assess your smile: tooth proportion, lip line, '
      'colour and the way your teeth meet.'),
     ('Design and preview', 'A digital or wax design lets you see the proposed shape before '
      'anything is changed.'),
     ('Preparation', 'A small amount of enamel is removed — often less than a millimetre — and '
      'an impression or scan is taken.'),
     ('Temporary veneers', 'You leave with temporaries so you are never without a smile, and so '
      'you can live with the new shape.'),
     ('Fitting', 'The veneers are tried in, checked with you in daylight, then bonded '
      'permanently.')],
   'faqs': [
     ('Are veneers reversible?',
      '<p>Generally no — a small amount of enamel is removed and does not grow back. That is why '
      'we plan carefully and consider whitening or bonding first where they would do the '
      'job.</p>'),
     ('How long do they last?',
      '<p>Well-made veneers commonly last ten to fifteen years or more. They can chip, so a '
      'night guard is advisable if you grind your teeth.</p>')],
 },

 'crowns': {
   'group': 'cosmetic', 'parent': 'cosmetic',
   'hero': 'images/heroes/cosmetic.jpg',
   'sub': 'Rebuilding a tooth that has lost too much of itself.',
   'lead': 'A crown is a type of dental restoration used to fix teeth that have been broken, '
           'weakened by decay or contain a very large filling.',
   'paras': [
     'A crown covers the whole visible part of a tooth, holding what is left of it together and '
     'restoring the shape and strength you had before. It is the usual next step when a filling '
     'would be too large to be reliable, or after root canal treatment on a back tooth.',
     'We offer same-day crowns crafted on site as well as laboratory-made crowns, and we will '
     'recommend the material — all-ceramic, eMax or metal-based — that suits the position, the '
     'load and the appearance you want.'],
   'image': 'images/cards/crowns.jpg',
   'process': [
     ('Assessment', 'We check whether a crown is the right answer, or whether a smaller '
      'restoration would do.'),
     ('Preparation', 'The tooth is shaped to make room for the crown, under local anaesthetic.'),
     ('Scan or impression', 'A digital scan records the shape precisely, along with how you '
      'bite.'),
     ('Same-day or laboratory', 'Same-day crowns are milled and fitted while you wait. '
      'Laboratory crowns take about two weeks, with a temporary in the meantime.'),
     ('Fitting and review', 'The crown is checked for fit, bite and colour, then cemented and '
      'reviewed.')],
   'faqs': [
     ('How long does a crown last?',
      '<p>Ten to fifteen years is typical, and often considerably longer with good hygiene. What '
      'usually fails first is the tooth underneath, not the crown itself.</p>'),
     ('Will it match my other teeth?',
      '<p>Shade is matched in daylight, and for front teeth we can arrange a shade appointment '
      'with the technician where the case calls for it.</p>')],
 },

 'bridges': {
   'group': 'cosmetic', 'parent': 'cosmetic',
   'hero': 'images/heroes/cosmetic.jpg',
   'sub': 'A fixed replacement anchored to the teeth beside the gap.',
   'lead': 'Losing a tooth through dental decay, gum disease or trauma can be devastating. A '
           'good solution is a dental bridge.',
   'paras': [
     'A bridge replaces one or more missing teeth by anchoring a replacement to the teeth either '
     'side of the gap. It is fixed in place — nothing to take out at night — and it stops the '
     'neighbouring teeth drifting into the space.',
     'Bridges suit some gaps better than others. Where the adjacent teeth are healthy and '
     'untouched, a dental implant may be the kinder long-term option, because it does not '
     'involve preparing them. We will set out both before you decide.'],
   'image': 'images/cards/bridges.jpg',
   'process': [
     ('Assessment', 'We check the health and position of the teeth either side of the gap, and '
      'the bone underneath.'),
     ('Choosing the design', 'Conventional, cantilever or adhesive (Maryland) bridges each suit '
      'different situations.'),
     ('Preparation', 'The supporting teeth are shaped where the design requires it.'),
     ('Laboratory work', 'The bridge is made by our technicians to match your existing teeth.'),
     ('Fitting', 'The bridge is tried in, adjusted and cemented, and we show you how to clean '
      'underneath it.')],
   'faqs': [
     ('Bridge or implant?',
      '<p>An implant leaves the neighbouring teeth untouched, which is a real advantage if they '
      'are healthy. A bridge is quicker and involves no surgery. See our '
      '<a class="link-inline" href="implant-clinic.html">implant clinic</a>.</p>'),
     ('How do I clean it?',
      '<p>With floss threaders or interdental brushes designed to reach underneath the false '
      'tooth. Our hygienist will show you.</p>')],
 },

 'whitening': {
   'group': 'cosmetic', 'parent': 'cosmetic',
   'hero': 'images/heroes/cosmetic.jpg',
   'sub': 'Dentist-supervised whitening, done gradually and safely.',
   'lead': 'If you are self-conscious about your teeth or you have staining on some teeth, '
           'professional teeth whitening treatment is an option.',
   'paras': [
     'We take impressions or a scan and make whitening trays moulded exactly to your teeth. You '
     'wear them at home with a measured amount of gel, usually over two to three weeks, and the '
     'colour lifts gradually rather than all at once.',
     'In the UK, tooth whitening is a dental procedure and it is illegal for anyone who is not a '
     'registered dental professional to provide it. Beauty-salon whitening and unregulated '
     'online kits carry a real risk of chemical burns and permanent sensitivity.'],
   'image': 'images/cards/teeth-whitening.jpg',
   'process': [
     ('Check-up first', 'Whitening goes on top of healthy teeth and gums. Any decay or gum '
      'problems are treated first.'),
     ('Custom trays', 'Trays made to your teeth keep the gel where it belongs and off your '
      'gums.'),
     ('Home whitening', 'You wear the trays for the time we specify, typically over two to '
      'three weeks.'),
     ('Managing sensitivity', 'Mild, temporary sensitivity is common. We can adjust the '
      'concentration or the wear time.'),
     ('Topping up', 'Keep the trays. A single top-up night every few months maintains the '
      'result at very little cost.')],
   'faqs': [
     ('Will it whiten crowns, veneers or fillings?',
      '<p>No. Whitening only works on natural tooth tissue. Existing restorations at the front '
      'may need replacing afterwards to match the new shade.</p>'),
     ('Is it safe?',
      '<p>Dentist-supervised whitening at regulated concentrations has a long safety record. The '
      'risk comes from unsupervised, over-strength products.</p>')],
 },

 'gum-reshaping': {
   'group': 'cosmetic', 'parent': 'cosmetic',
   'hero': 'images/heroes/cosmetic.jpg',
   'sub': 'Healthy gums first, then an even gum line.',
   'lead': 'Periodontics focuses on the health and treatment of gums and bones, working to '
           'correct and prevent damage.',
   'paras': [
     'The gum line frames the teeth. An uneven line, or gums that show more than you would like '
     'when you smile, can make well-shaped teeth look short or irregular. Reshaping evens that '
     'frame out.',
     'It is also a health treatment, not only a cosmetic one. Periodontal disease destroys the '
     'bone that holds teeth in place, and it is the most common reason adults lose teeth. '
     'Treating and stabilising the gums always comes before any cosmetic reshaping.'],
   'image': 'images/cards/gum-reshaping.jpg',
   'process': [
     ('Periodontal assessment', 'We measure the gum pockets around every tooth and take '
      'radiographs to check the bone level.'),
     ('Stabilise first', 'Any active gum disease is treated and brought under control before '
      'reshaping is considered.'),
     ('Planning the gum line', 'We plan the finished line against your lip position and tooth '
      'proportions.'),
     ('Reshaping', 'Excess tissue is contoured under local anaesthetic. Healing is usually '
      'straightforward.'),
     ('Maintenance', 'Regular hygiene visits keep the result stable.')],
   'faqs': [
     ('Is the treatment painful?',
      '<p>It is carried out under local anaesthetic. Expect some tenderness for a few days '
      'afterwards, managed with ordinary painkillers.</p>'),
     ('Will the gums grow back?',
      '<p>Where the underlying bone has been recontoured the result is stable. Good hygiene and '
      'regular maintenance are what protect it.</p>')],
 },

 'check-up': {
   'group': 'preventative', 'parent': 'preventative',
   'hero': 'images/heroes/preventative.jpg',
   'sub': 'The appointment that keeps the others short.',
   'lead': 'A standard dental check-up is carried out by our experienced, qualified dentist and '
           'is the best way to spot any problems with your mouth before they become serious.',
   'paras': [
     'A check-up is much more than a quick look at your teeth. We examine the soft tissues, the '
     'gums, your bite and any existing restorations, and we screen for oral cancer at every '
     'appointment.',
     'Most problems we find at a check-up are small, cheap and painless to deal with. The same '
     'problems found two years later are often none of those things. That is the whole argument '
     'for coming regularly.'],
   'image': 'images/cards/check-up.jpg',
   'process': [
     ('Medical history', 'We check what has changed — medication, health conditions, anything '
      'that affects your mouth.'),
     ('Examination', 'Teeth, existing fillings and crowns, gums, tongue, cheeks and the soft '
      'tissues, plus an oral cancer screen.'),
     ('Radiographs when needed', 'X-rays are taken at intervals appropriate to your risk, not '
      'automatically at every visit.'),
     ('Findings explained', 'You are told what we found, in plain language, with the options '
      'and the costs.'),
     ('Recall interval', 'We set your next visit by your individual risk — commonly six months, '
      'sometimes three, sometimes twelve.')],
   'faqs': [
     ('How often should I come?',
      '<p>Between three and twenty-four months, depending on your risk. Members of Our Plan '
      'have two visits a year included.</p>'),
     ('What is included in my plan?',
      '<p>Two dentist visits and two hygiene visits a year, all necessary X-rays and 10% off '
      'any treatment. See <a class="link-inline" href="fees-and-membership.html">fees and '
      'membership</a>.</p>')],
 },

 'hygiene': {
   'group': 'preventative', 'parent': 'preventative',
   'hero': 'images/heroes/preventative.jpg',
   'sub': 'Removing what a toothbrush cannot reach.',
   'lead': 'Dental hygiene treatment is delivered by a specially trained professional who will '
           'help to remove any hard-to-reach plaque from your teeth that may have built up over '
           'time.',
   'paras': [
     'Plaque that is not removed hardens into calculus within a couple of days, and once it has '
     'hardened no amount of brushing will shift it. Left in place it irritates the gums, and '
     'over time it destroys the bone underneath.',
     'A hygiene visit removes that build-up above and below the gum line, polishes the teeth, '
     'and — just as importantly — shows you where your own cleaning is missing. Most people are '
     'brushing well; almost everyone is missing the same two or three places.'],
   'image': 'images/cards/dental-hygiene.jpg',
   'process': [
     ('Gum assessment', 'Pocket depths and bleeding points are recorded so progress can be '
      'measured objectively.'),
     ('Scaling', 'Hard deposits are removed from above and below the gum line with ultrasonic '
      'and hand instruments.'),
     ('Polishing', 'Surface staining from tea, coffee, red wine and tobacco is removed.'),
     ('Technique coaching', 'We show you exactly where you are missing, and which interdental '
      'brush size fits each gap.'),
     ('Interval', 'Most people benefit from two visits a year. Where there is active gum '
      'disease, three or four is more effective.')],
   'faqs': [
     ('Does it hurt?',
      '<p>Usually not, though it can be uncomfortable if the gums are inflamed. Anaesthetic gel '
      'or local anaesthetic is available.</p>'),
     ('My gums bleed when I brush. Should I stop?',
      '<p>No — bleeding gums are inflamed gums, and stopping makes it worse. Keep cleaning '
      'gently and thoroughly, and come and see us.</p>')],
 },

 'sensitive': {
   'group': 'preventative', 'parent': 'preventative',
   'hero': 'images/heroes/preventative.jpg',
   'sub': 'Sensitivity is a symptom. It is worth finding the cause.',
   'lead': 'Do you feel a shooting pain in your teeth when eating or drinking something hot? '
           'Does the thought of biting into an ice cream or a cold, hard apple make you wince?',
   'paras': [
     'Sensitivity happens when the dentine underneath the enamel is exposed — through gum '
     'recession, worn enamel, a cracked tooth, decay, or a failing filling. Each of those has a '
     'different answer.',
     'Desensitising toothpaste helps a good many people and it is a sensible first step. But '
     'sensitivity that is getting worse, is confined to one tooth, or lingers after the '
     'stimulus has gone is worth investigating properly rather than masking.'],
   'image': 'images/cards/sensitive-teeth.jpg',
   'process': [
     ('Find the cause', 'We test individual teeth to identify whether the problem is generalised '
      'or coming from one place.'),
     ('Treat what we find', 'Recession, a cracked cusp, decay and a leaking filling all need '
      'different treatment.'),
     ('Protect the enamel', 'Acid erosion from fizzy drinks, citrus and reflux is a common '
      'cause and is preventable.'),
     ('Fluoride and desensitisers', 'Professional applications work considerably faster than '
      'toothpaste alone.'),
     ('Check for grinding', 'Night-time clenching wears enamel and flexes teeth at the gum '
      'line. A guard protects them.')],
   'faqs': [
     ('Should I brush harder?',
      '<p>No. Hard brushing with a stiff brush is one of the more common causes of the recession '
      'that leads to sensitivity. A soft brush used thoroughly is better.</p>'),
     ('When should I be concerned?',
      '<p>If the pain lingers for more than a few seconds, wakes you at night, or is confined to '
      'a single tooth, please book an appointment.</p>')],
 },
}


# =============================================================================
# CATEGORY PAGES (General / Cosmetic / Preventative / Missing teeth)
# =============================================================================
CATEGORY = {
 'general': {
   'hero': 'images/heroes/general.jpg',
   'sub': 'We are your trusted local family dental practice for all kinds of general dentistry.',
   'lead': 'General dentistry is the everyday care that keeps a mouth working: diagnosing what is '
           'wrong, fixing it properly, and keeping it that way.',
   'paras': [
     'It covers examinations, fillings, root canal treatment, extractions and the emergency care '
     'you hope never to need. Most of it is unglamorous, and all of it matters more than any '
     'cosmetic treatment we offer.',
     'We see whole families here — children, parents and grandparents — often on the same '
     'afternoon. Whatever brings you in, you will be told what we find, what your options are '
     'and what each one costs, before anything is agreed.'],
   'image': 'images/cards/general-dentistry.jpg',
   'children': ['root-canal', 'extractions', 'emergency', 'nervous'],
   'card_images': {'root-canal': 'images/cards/root-canal-therapy.jpg',
                   'extractions': 'images/cards/extractions.jpg',
                   'emergency': 'images/cards/emergency-dental-treatment.jpg',
                   'nervous': 'images/cards/nervous-patients.jpg'},
   'card_text': {
     'root-canal': 'Root canal treatment is available at the practice. Following an initial '
                   'assessment, some cases are better referred to a specialist endodontist.',
     'extractions': 'In cases of advanced gum disease and tooth decay, teeth may need to be '
                    'extracted. Some patients also develop impacted wisdom teeth.',
     'emergency': 'If you have chipped or broken a tooth as a result of an accident or injury, '
                  'it is very important that you see a dentist as soon as possible.',
     'nervous': 'We understand that you may not like coming to the dentist. Don’t worry — '
                'you’re not alone, and we will go entirely at your pace.'},
   'process': [
     ('Examination', 'A full assessment of teeth, gums and soft tissues, with radiographs where '
      'they are needed.'),
     ('Diagnosis in plain English', 'You are shown what we have found — on screen where that '
      'helps — and what it means.'),
     ('Options and costs', 'Every reasonable option is set out with its cost, including doing '
      'nothing for now where that is safe.'),
     ('Treatment', 'Carried out at a pace that suits you, in as few visits as the work sensibly '
      'allows.'),
     ('Review and prevention', 'We agree a recall interval based on your individual risk, not a '
      'blanket six months.')],
 },
 'cosmetic': {
   'hero': 'images/heroes/cosmetic.jpg',
   'sub': 'Treatments that enhance, align, and whiten or tone your teeth for a more attractive '
          'appearance.',
   'lead': 'Not everyone is happy with their smile or how their teeth look. This can have a '
           'major impact on a person’s confidence when it comes to interacting and socialising '
           'with others.',
   'paras': [
     'Cosmetic dentistry is a field within general dentistry that focuses on the beauty of a '
     'smile. It covers treatments that enhance, align, and whiten or tone the teeth — porcelain '
     'veneers, crowns, bridges, teeth whitening, gum reshaping and orthodontics.',
     'These treatments involve special techniques, equipment and a high level of skill from the '
     'dental team. We are proud to offer them to our patients here at the practice, and have '
     'seen many a smile transformed under our own roof.',
     'If you are embarrassed by your teeth it is best to speak to your dentist, who can tell you '
     'more about the options available in a non-judgemental and empathetic environment.'],
   'image': 'images/cards/family-smiles.jpg',
   'children': ['clear-aligner', 'veneers', 'crowns', 'bridges', 'whitening', 'gum-reshaping'],
   'card_images': {'clear-aligner': 'images/cards/clear-aligners.jpg',
                   'veneers': 'images/cards/veneers.jpg',
                   'crowns': 'images/cards/crowns.jpg',
                   'bridges': 'images/cards/bridges.jpg',
                   'whitening': 'images/cards/teeth-whitening.jpg',
                   'gum-reshaping': 'images/cards/gum-reshaping.jpg'},
   'card_text': {
     'clear-aligner': 'Invisible orthodontics is a solution to having straighter teeth without '
                      'having to wear metal braces.',
     'veneers': 'Are your teeth stained, chipped, or not aligned on top of each other? Veneers '
                'are an option to consider.',
     'crowns': 'A crown is a type of dental restoration used to fix teeth that have been broken, '
               'weakened by decay or contain a very large filling.',
     'bridges': 'Losing a tooth through dental decay, gum disease or trauma can be devastating. '
                'A good solution is a dental bridge.',
     'whitening': 'If you are self-conscious about your teeth or you have staining on some '
                  'teeth, professional whitening treatment is an option.',
     'gum-reshaping': 'Periodontics focuses on the health and treatment of gums and bones, '
                      'working to correct and prevent damage.'},
   'process': [
     ('Talk it through', 'What is it that bothers you? Naming it precisely is what makes a good '
      'plan possible.'),
     ('Assessment and records', 'Photographs, a scan and an examination of the gums and bite — '
      'cosmetic work only lasts on a healthy foundation.'),
     ('Design', 'A digital or wax-up preview so you can see the proposed result before any tooth '
      'is touched.'),
     ('Agree the plan', 'A written plan with the sequence, the number of visits and a fully '
      'costed quotation.'),
     ('Treatment and review', 'Carried out in stages, with a review once everything has '
      'settled.')],
 },
 'preventative': {
   'hero': 'images/heroes/preventative.jpg',
   'sub': 'Routine dental appointments are essential to maintain good oral health and a happy '
          'smile.',
   'lead': 'Preventative dentistry is the least dramatic thing we do and by far the most '
           'valuable.',
   'paras': [
     'Regular check-ups and hygiene visits catch decay while it is still a small filling, catch '
     'gum disease while it is still reversible, and catch the rarer, more serious things early '
     'enough to matter.',
     'As part of our focus on preventative dentistry we offer Our Plan, a dental payment plan '
     'that covers the cost of your preventative dental care. We believe this is a fair way of '
     'encouraging regular dental attendance and, therefore, helping to keep you in good dental '
     'health.'],
   'image': 'images/cards/preventative-dentistry.jpg',
   'children': ['check-up', 'hygiene', 'sensitive'],
   'card_images': {'check-up': 'images/cards/check-up.jpg',
                   'hygiene': 'images/cards/dental-hygiene.jpg',
                   'sensitive': 'images/cards/sensitive-teeth.jpg'},
   'card_text': {
     'check-up': 'A standard dental check-up is carried out by our experienced, qualified '
                 'dentist to spot any problems with your mouth before they become serious.',
     'hygiene': 'Dental hygiene treatment is delivered by a specially trained professional who '
                'will help to remove hard-to-reach plaque from your teeth.',
     'sensitive': 'Do you feel a shooting pain in your teeth when eating or drinking something '
                  'hot or cold? Does biting into an ice cream make you wince?'},
   'process': [
     ('Two dentist visits a year', 'Included in Our Plan, with all necessary X-rays.'),
     ('Two hygiene visits a year', 'Assessment and maintenance to keep the gums stable.'),
     ('Preventative and dietary advice', 'Practical, specific advice about your own habits — not '
      'a leaflet.'),
     ('Fluoride and sealants', 'Particularly valuable for children and for anyone at higher '
      'risk of decay.'),
     ('Emergency access', 'Same day or next day emergency appointments, with a £0 access fee '
      'for plan members.')],
 },
 'missing': {
   'hero': 'images/heroes/missing.jpg',
   'sub': 'Crowns, bridges, dentures and implants — the options, explained clearly.',
   'lead': 'A missing tooth is not only a cosmetic problem. The teeth either side drift, the '
           'opposing tooth over-erupts, and the bone that used to support the root begins to '
           'shrink away.',
   'paras': [
     'There is rarely only one right answer. A single gap at the back of the mouth may need '
     'nothing at all. A gap at the front almost always needs something. Between those extremes '
     'sit crowns, bridges, partial and full dentures, and implant-supported solutions.',
     'We will assess the gap, the neighbouring teeth, the bone underneath and how you bite, then '
     'set out each realistic option with its advantages, its limitations, its likely lifespan '
     'and its cost. You decide from there — there is no hard sell.'],
   'image': 'images/cards/implant-clinic-feature.jpg',
   'children': [],
   'card_images': {}, 'card_text': {},
   'process': [
     ('Assessment', 'Radiographs, and a CBCT scan where implants are being considered, to see '
      'the bone in three dimensions.'),
     ('Crowns', 'Where enough of the natural tooth remains, a crown rebuilds it rather than '
      'replacing it.'),
     ('Bridges', 'A fixed replacement anchored to the teeth either side of the gap — no surgery, '
      'nothing to take out.'),
     ('Dentures', 'Removable, and by far the most economical way to replace several teeth. '
      'Modern designs are a long way from what they once were.'),
     ('Dental implants', 'A titanium root placed in the jaw. The only option that replaces the '
      'root as well as the tooth, and the only one that preserves the bone.')],
 },
}


# =============================================================================
# CASE STUDIES
# =============================================================================
CASES = [
 {'key': 'case-worn',
  'thumb': 'placeholder-case-worn.jpg',
  'teaser': 'Over time, tooth wear and tear can significantly affect both the appearance and '
            'function of the smile. In this case, the patient presented with generalised worn '
            'dentition, visible crack lines, and concerns about the overall aesthetics of his '
            'teeth.',
  'label': 'Composite bonding',
  'body': [
    ('h2', 'The presentation'),
    ('p', 'Over time, tooth wear and tear can significantly affect both the appearance and '
          'function of the smile. In this case, the patient presented with generalised worn '
          'dentition, visible crack lines, and concerns about the overall aesthetics of his '
          'teeth.'),
    ('p', 'Following a comprehensive clinical assessment, a range of treatment options were '
          'carefully discussed. These included:'),
    ('ul', ['Occlusal management and monitoring', 'Composite bonding', 'Porcelain veneers',
            'Full-coverage restorations such as crowns']),
    ('p', 'Each option was explained in detail, outlining the benefits, limitations, longevity '
          'and level of invasiveness, allowing the patient to make a fully informed decision.'),
    ('h2', 'Digital planning and conservative treatment'),
    ('p', 'After careful digital planning, which included analysis of tooth wear, bite position '
          'and smile proportions, the patient elected to proceed with minimally invasive '
          'composite bonding. This approach aligned with his desire to preserve as much natural '
          'tooth structure as possible while still achieving a noticeable aesthetic and '
          'functional improvement.'),
    ('p', 'Composite bonding allowed us to:'),
    ('ul', ['Restore worn tooth surfaces', 'Mask visible crack lines where appropriate',
            'Rebuild tooth length and shape', 'Improve symmetry and smile balance',
            'Protect teeth from further wear']),
    ('p', 'The treatment was guided precisely by the digital plan, ensuring predictable results '
          'and a natural finish.'),
    ('h2', 'The outcome'),
    ('p', 'The final result delivered a refreshed, natural-looking smile with improved function '
          'and aesthetics — without the need for aggressive tooth preparation. The patient was '
          'extremely pleased with both the process and the outcome, reporting that he does not '
          'regret choosing composite bonding and is very happy with his decision.'),
    ('h2', 'A thoughtful, patient-led choice'),
    ('p', 'This case highlights how minimally invasive dentistry, supported by modern digital '
          'planning, can offer excellent results even in cases of significant tooth wear. While '
          'more extensive options were available, composite bonding proved to be the right '
          'solution for this patient at this stage of his dental journey.'),
  ],
  'shots': [('images/cases/case-worn-1.jpg', 'Before', 'Worn front teeth before treatment'),
            ('images/cases/case-worn-2.jpg', 'After', 'Composite bonding completed'),
            ('images/cases/case-worn-3.jpg', 'Detail', 'Close-up of the finished bonding')]},

 {'key': 'case-missing',
  'thumb': 'placeholder-case-missing.jpg',
  'label': 'Veneers, crowns & denture',
  'teaser': 'The patient came to see us as a self-referral, unsatisfied with the appearance of '
            'his front teeth and dissatisfied with previous “patch up work” on his front teeth.',
  'body': [
    ('h2', 'The presentation'),
    ('p', 'The patient came to see us as a self-referral, unsatisfied with the appearance of his '
          'front teeth and dissatisfied with previous “patch up work” on his front teeth.'),
    ('h2', 'Planning and options'),
    ('p', 'After meticulous planning and discussion of ALL options to improve function and '
          'aesthetic appearance of the remaining teeth, the patient decided to have treatment in '
          'the upper jaw only, involving provision of 2 new eMax veneers and 2 new eMax crowns '
          'combined with a partial metal based upper denture.'),
    ('h2', 'The outcome'),
    ('p', 'The combination restored both the appearance and the function of the upper arch while '
          'keeping the treatment within the scope the patient had chosen. The patient was very '
          'happy with the result.'),
  ],
  'shots': [('images/cases/case-missing-1.jpg', 'Before', 'Front teeth before treatment'),
            ('images/cases/case-missing-2.jpg', 'After', 'Completed veneers, crowns and denture')]},

 {'key': 'case-newdenture',
  'thumb': 'placeholder-case-newdenture.jpg',
  'label': 'Denture',
  'teaser': '82 year old female patient came to see us requesting a new upper denture. After '
            'meticulous treatment planning, the patient decided to have the BEST possible '
            'denture without use of dental implants.',
  'body': [
    ('h2', 'The presentation'),
    ('p', '82 year old female patient came to see us requesting a new upper denture.'),
    ('h2', 'Planning and options'),
    ('p', 'After a meticulous treatment planning process, the patient decided to have the BEST '
          'possible denture without the use of dental implants. Every option was set out — '
          'including implant-retained alternatives — before the decision was made.'),
    ('h2', 'The outcome'),
    ('p', 'A precision metal-based denture was constructed with our laboratory partners, '
          'restoring both appearance and chewing function while remaining entirely '
          'non-surgical.'),
  ],
  'shots': [('images/cases/case-newdenture-1.jpg', 'Before', 'Upper arch before treatment'),
            ('images/cases/case-newdenture-2.jpg', 'Before', 'Existing restorations'),
            ('images/cases/case-newdenture-3.jpg', 'After', 'Completed denture in place'),
            ('images/cases/case-newdenture-4.jpg', 'After', 'The finished metal-based denture')]},

 {'key': 'case-loose',
  'thumb': 'placeholder-case-loose.jpg',
  'label': 'Implants',
  'teaser': 'Patient came to see us unhappy about a loose upper denture. Following a meticulous '
            'treatment planning process, the patient decided to have 4 dental implants placed '
            'supporting screw retained / non removable 10 new teeth with no palatal coverage.',
  'body': [
    ('h2', 'The presentation'),
    ('p', 'The patient came to see us unhappy about a loose upper denture — a common and '
          'genuinely difficult problem, affecting confidence in eating and in speaking.'),
    ('h2', 'Planning and options'),
    ('p', 'Following a meticulous treatment planning process, the patient decided to have 4 '
          'dental implants placed, supporting screw retained / non removable 10 new teeth with '
          'no palatal coverage.'),
    ('h2', 'The outcome'),
    ('p', 'Removing the palatal coverage restores the sense of taste and temperature that a full '
          'upper denture takes away, and a screw-retained bridge does not move. The patient '
          'reported a substantial improvement in both function and confidence.'),
  ],
  'shots': [('images/cases/case-loose-1.jpg', 'Before', 'Upper arch before treatment'),
            ('images/cases/case-loose-2.jpg', 'Before', 'The existing loose denture'),
            ('images/cases/case-loose-3.jpg', 'During', 'Four implants placed'),
            ('images/cases/case-loose-4.jpg', 'During', 'The prosthesis being fitted'),
            ('images/cases/case-loose-5.jpg', 'After', 'The completed result'),
            ('images/cases/case-loose-6.jpg', 'After', 'The finished smile')]},

 {'key': 'case-sameday',
  'thumb': 'placeholder-case-sameday.jpg',
  'label': 'Same day teeth',
  'teaser': 'Patient came to see us with 6 teeth remaining in the lower jaw. Until this moment '
            'the patient could manage. Unfortunately the bridge was beyond repair and the '
            'patient faced some tough decisions.',
  'body': [
    ('h2', 'The presentation'),
    ('p', 'The patient came to see us with 6 teeth remaining in the lower jaw. Until this moment '
          'the patient could manage. Unfortunately the bridge was beyond repair and the patient '
          'faced some tough decisions.'),
    ('h2', 'Planning and options'),
    ('p', 'Every option was discussed in full, including a conventional lower denture. The '
          'patient chose an implant-supported solution allowing a fixed set of teeth to be '
          'delivered without a prolonged period without teeth.'),
    ('h2', 'The outcome'),
    ('p', 'The result restored a full lower arch with a fixed, implant-supported prosthesis, and '
          'with it the ability to eat and speak with confidence.'),
  ],
  'shots': [('images/cases/case-sameday-1.jpg', 'Before', 'Lower arch before treatment'),
            ('images/cases/case-sameday-2.jpg', 'Before', 'The failing bridge'),
            ('images/cases/case-sameday-3.jpg', 'During', 'The provisional prosthesis'),
            ('images/cases/case-sameday-4.jpg', 'During', 'The prosthesis on the bench'),
            ('images/cases/case-sameday-5.jpg', 'After', 'The completed result'),
            ('images/cases/case-sameday-6.jpg', 'After', 'The finished prosthesis')]},
]
CASE_BY_KEY = dict((c['key'], c) for c in CASES)

# =============================================================================
# TESTIMONIALS — as published on the current site
# =============================================================================
TESTIMONIALS = [
 ('My experience at your practice can only be described as beyond perfect. From the initial '
  'consultation, through to the preparation and procedure was very professional and impressive. '
  'Martin Sulo is undoubtedly a top man in his profession. The whole procedure was painless and '
  'very thorough. Although my bank account has taken a hammering of late, the whole procedure '
  'has been more than worthwhile and I am now reaping the benefits.', 'David Wattam'),
 ('Been using the surgery for near on 20 years. Great people, honest and always helpful. Denplan '
  'works for me so cost is per month and covers everything. Very happy visiting and always leave '
  'with a smile.', 'Darren Gundry'),
 ('Just to say a huge thank you to Martin, Eve and all the team for your dedication, skill and '
  'utmost care. Thank you all.', 'Val Forge'),
 ('I’m no longer fearful of coming to the dentist. The team put me at ease from the first '
  'appointment and explained everything as we went along.', 'Practice patient'),
]


# =============================================================================
# FORM BUILDERS
# =============================================================================
def f_field(fid, label, kind='text', required=False, full=False, hint='', options=None,
            placeholder='', rows=4, name=None):
    """`name` defaults to the id. Pass it separately only for repeat-group
    fields, where the id is base-i-suffix but the name is base[i][suffix]."""
    req = ' required' if required else ''
    star = ' <span class="field__req" aria-hidden="true">*</span>' if required else ''
    cls = 'field field--full' if full else 'field'
    ph = ' placeholder="%s"' % _e(placeholder) if placeholder else ''
    nm = name if name is not None else fid

    if kind == 'textarea':
        control = '<textarea id="%s" name="%s" rows="%d"%s%s></textarea>' % (fid, nm, rows, req, ph)
    elif kind == 'select':
        opts = ['<option value="" disabled selected>Please choose</option>']
        opts += ['<option>%s</option>' % _e(o) for o in (options or [])]
        control = '<select id="%s" name="%s"%s>%s</select>' % (fid, nm, req, ''.join(opts))
    else:
        control = '<input id="%s" name="%s" type="%s"%s%s>' % (fid, nm, kind, req, ph)

    hint_html = '<span class="field__hint">%s</span>' % _e(hint) if hint else ''
    return ('<div class="%s"><label for="%s">%s%s</label>%s%s'
            '<span class="field__error" role="alert"></span></div>'
            % (cls, fid, _e(label), star, control, hint_html))


def f_checks(name, legend, options, kind='checkbox'):
    items = ''.join(
        '<label class="choice"><input type="%s" name="%s" value="%s"><span>%s</span></label>'
        % (kind, name, _e(o), _e(o)) for o in options)
    return ('<fieldset class="fieldset field--full"><legend class="fieldset__legend">%s</legend>'
            '<div class="choice-grid">%s</div></fieldset>' % (_e(legend), items))


def f_step(title, fields, intro=''):
    """One panel of a multi-step form.

    Rendered as a plain <div>, so with JavaScript off every step is simply
    visible and the form reads as one long page. js/forms.js turns the set into
    a wizard — see the header of that file.
    """
    lead = '<p class="form__step-intro field__hint">%s</p>' % intro if intro else ''
    return ('<div class="form__step" data-step data-step-title="%s">\n'
            '    <div class="form__section-title">%s</div>%s\n'
            '    <div class="form__grid">\n      %s\n    </div>\n  </div>'
            % (_e(title), _e(title), lead, '\n      '.join(fields)))


def f_repeat(base, singular, fields, min_items=1, max_items=12, add_label=None):
    """A variable-length list of identical field sets — an "array" group.

    `fields` is a callable taking an index token and returning the field HTML
    for one item. Both the first (index 0) item and the <template> used for
    every later one are built from it, so the two can never drift apart.

    Controls are named  base[i][suffix]  and given ids  base-i-suffix, which
    js/forms.js renumbers on add and remove so the indices stay 0..n-1.
    """
    def item(index, number):
        return (
            '<div class="repeat__item" data-repeat-item>\n'
            '        <div class="repeat__head">\n'
            '          <span class="repeat__num">%s <span data-repeat-num>%s</span></span>\n'
            '          <button class="repeat__remove" type="button" data-repeat-remove>Remove</button>\n'
            '        </div>\n'
            '        <div class="form__grid">\n          %s\n        </div>\n'
            '      </div>' % (_e(singular), number, '\n          '.join(fields(index))))

    return (
        '<div class="repeat" data-repeat data-repeat-name="%s" data-repeat-singular="%s" '
        'data-repeat-min="%d" data-repeat-max="%d">\n'
        '      <div class="repeat__list" data-repeat-list>\n      %s\n      </div>\n'
        '      <template data-repeat-template>%s</template>\n'
        '      <button class="btn btn--outline btn--sm repeat__add" type="button" data-repeat-add>'
        '<span class="btn__fill"></span><span class="btn__label">%s</span></button>\n'
        '      <p class="repeat__full" data-repeat-full hidden>That is the maximum of %d. '
        'Please contact the practice if you need to add more.</p>\n'
        '      <p class="visually-hidden" role="status" data-repeat-status></p>\n'
        '    </div>'
        % (base, _e(singular), min_items, max_items,
           item('0', '01'), item('__i__', '__n__'),
           _e(add_label or ('Add another ' + singular.lower())), max_items))


def f_chooser(cid, panels):
    """Tab switcher for a page holding one form per audience.

    `panels` is a list of (key, tab title, tab subtitle, heading, body). The tab
    row ships hidden and every panel ships visible, so with JavaScript off the
    page is exactly what it was before — two headed forms, one after the other.
    js/ui.js unhides the tabs and takes over from there.
    """
    tabs = ''.join(
        '<button class="chooser__tab" type="button" role="tab" id="%s-tab-%s" '
        'aria-controls="%s-panel-%s" aria-selected="%s" data-chooser-key="%s" tabindex="%s">'
        '<span class="chooser__tab-title">%s</span>'
        '<span class="chooser__tab-sub">%s</span></button>'
        % (cid, key, cid, key, 'true' if i == 0 else 'false', key, '0' if i == 0 else '-1',
           _e(title), _e(sub))
        for i, (key, title, sub, _h, _b) in enumerate(panels))

    bodies = '\n'.join(
        '<div class="chooser__panel" id="%s-panel-%s" role="tabpanel" '
        'aria-labelledby="%s-tab-%s" tabindex="0">\n'
        '  <h2 class="chooser__heading u-mb-6">%s</h2>\n  %s\n</div>'
        % (cid, key, cid, key, _e(heading), body)
        for key, _t, _s, heading, body in panels)

    return ('<div class="chooser" data-chooser>\n'
            '  <div class="chooser__tabs" role="tablist" aria-label="Who is referring?" hidden>%s</div>\n'
            '%s\n</div>' % (tabs, bodies))


def f_form(form_id, fields, submit='Send', note='', success_title='Thank you — message sent.',
           success_text='A member of the practice team will be in touch shortly.',
           steps=False):
    """`fields` is either a flat list of field HTML, or — when steps=True — a
    list of f_step() panels."""
    sid = form_id + 'Success'
    if steps:
        body = '\n  '.join(fields)
        attrs = ' data-steps'
    else:
        body = '<div class="form__grid">\n    %s\n  </div>' % '\n    '.join(fields)
        attrs = ''

    return '''<form class="form" id="{fid}" data-validate{attrs} data-success="{sid}" novalidate>
  {body}
  <div class="form__actions">
    <button class="btn btn--solid" type="submit"><span class="btn__fill"></span><span class="btn__label">{submit}</span></button>
    {note}
  </div>
</form>
<div class="form__success" id="{sid}" hidden>
  <h3>{stitle}</h3>
  <p>{stext}</p>
</div>'''.format(fid=form_id, sid=sid, body=body, attrs=attrs, submit=_e(submit),
                 note=('<p class="form__note">%s</p>' % note) if note else '',
                 stitle=_e(success_title), stext=_e(success_text))


# =============================================================================
# PAGE RENDERERS
# =============================================================================
def render_body(key, page, depth, H):
    if key in LEAF:
        return r_leaf(key, depth, H)
    if key in CATEGORY:
        return r_category(key, depth, H)
    if key in CASE_BY_KEY:
        return r_case(key, depth, H)
    return globals()['r_' + key.replace('-', '_')](depth, H)


# ---- Generic: leaf treatment page -------------------------------------------
def r_leaf(key, depth, H):
    d = LEAF[key]
    parent = d['parent']
    crumbs = c_crumbs(H, depth, ['treatments', parent], LABELS[key])
    out = [c_page_head(H, depth, LABELS[parent], LABELS[key], d['sub'], d['hero'], crumbs)]

    rail = c_rail(H, depth, key, d['group'])
    prose = ['<p class="statement-text statement-text--wide">%s</p>' % _e(d['lead'])]
    prose += ['<p>%s</p>' % p for p in d['paras']]
    if d.get('image'):
        prose.append('<figure class="figure u-mt-8">%s<figcaption>%s</figcaption></figure>'
                     % (c_ph(LABELS[key], 'ar-3-2'), _e(LABELS[key])))

    out.append(c_section(
        '<div class="with-rail"><div class="prose">%s</div>%s</div>'
        % (''.join(prose), rail)))

    out.append(c_process(H, depth, 'What to expect', 'How it works', d['process']))

    if d.get('faqs'):
        out.append(c_section(
            '<div class="section-head"><span class="label">Common questions</span>'
            '<h2>Good to know</h2></div>'
            + c_accordion(d['faqs'], idbase=key), cls='section--paper-3'))

    out.append(c_cta(H, depth, 'Ready when you are.',
                     'Call the practice on %s or send us a message and we will get back to you.'
                     % SITE['phone'],
                     secondary=('All treatments', 'treatments')))
    return '\n'.join(out)


# ---- Generic: category page --------------------------------------------------
def r_category(key, depth, H):
    d = CATEGORY[key]
    crumbs = c_crumbs(H, depth, ['treatments'], LABELS[key])
    out = [c_page_head(H, depth, 'Treatments', LABELS[key], d['sub'], d['hero'], crumbs)]

    out.append(c_ed(H, depth, LABELS[key], d['lead'], d['paras'],
                    image=d.get('image'), alt=LABELS[key]))

    if d['children']:
        items = [{'key': k, 'label': LABELS[k], 'title': LABELS[k],
                  'text': d['card_text'][k], 'image': d['card_images'][k], 'alt': LABELS[k]}
                 for k in d['children']]
        cols = 3 if len(items) != 4 else 4
        out.append(c_strip(H, depth, 'In this section', 'What we offer', items, cols=cols))

    out.append(c_process(H, depth, 'The process', 'How treatment works here', d['process']))

    if key == 'missing':
        out.append(c_statement(
            H, depth, 'Implant clinic',
            'Implants are the only option that replaces the root as well as the tooth.',
            'Implant dentistry offers a clinically proven and safe solution to getting a great '
            'smile back and being able to bite and chew with confidence.',
            facts=[('3D', 'CBCT planning'), ('In-house', 'Placement & restoration'),
                   ('£0', 'Referral fee for plan members')],
            link=('Visit the implant clinic', H.rel('implant', depth))))

    out.append(c_quote(TESTIMONIALS[:3]))
    out.append(c_cta(H, depth, 'Ready when you are.',
                     secondary=('Fees and membership', 'fees')))
    return '\n'.join(out)


# ---- Home --------------------------------------------------------------------
def r_home(depth, H):
    out = []
    out.append(c_hero(
        H, depth, 'Botesdale, Suffolk',
        'A calmer kind<br>of dental care.',
        'Family dentistry, cosmetic treatment and advanced implant work — all under one roof, '
        'in a purpose-built practice in the heart of the village.',
        'images/heroes/home.jpg',
        actions=c_btn('Book a visit', H.rel('contact', depth), 'light')
                + c_btn('Fees and membership', H.rel('fees', depth), 'light')))

    tabs = [('care', 'Care'), ('team', 'Team'), ('plan', 'Plan'), ('visit', 'Visit')]
    tabnav = ''.join(
        '<a class="tab" href="#%s" data-target="%s"><span>%s</span>%s</a>' % (t, t, l, ARC)
        for t, l in tabs)

    blocks = []
    blocks.append('<div class="tabnav"><div class="tabnav__inner">%s</div></div>' % tabnav)

    blocks.append('<div id="care">' + c_ed(
        H, depth, 'Philosophy',
        'Modern, patient-centred care in a relaxed and friendly environment.',
        ['Botesdale Dental Practice &amp; Implant Clinic is dedicated to providing high-quality '
         'care in a relaxed and friendly environment. From routine family dentistry to advanced '
         'implant treatments, everything happens under one roof.',
         'Our experienced team combines clinical excellence with a gentle, compassionate '
         'approach, so that every patient feels comfortable and confident in their care.'],
        link=('View treatments', H.rel('treatments', depth)),
        image='images/cards/family-group.jpg', alt='A family smiling together') + '</div>')

    blocks.append('<div id="team">' + c_ed(
        H, depth, 'Since 2010', 'A family-run practice, in a purpose-built home.',
        ['Founded in 2010 by experienced dentist Dr Martin Sulo and managed alongside his wife '
         'Eve Sulo, the practice moved into a purpose-built, state-of-the-art facility in the '
         'heart of Botesdale in September 2024.',
         'The new building reflects everything we stand for: quality, accessibility, comfort and '
         'clinical excellence — fully accessible, thoughtfully designed and equipped with the '
         'latest dental technology.'],
        link=('Meet the team', H.rel('about', depth)),
        image='images/cards/practice-1.jpg', alt='The practice building',
        rev=True, warm=True) + '</div>')

    blocks.append('<div id="plan">' + c_statement(
        H, depth, 'Membership',
        'Our Plan. Built for regular care, not surprise bills.',
        'As part of our focus on preventative dentistry we offer Our Plan, a dental payment plan '
        'that covers the cost of your preventative dental care — a fair way of encouraging '
        'regular attendance and keeping you in good dental health.',
        facts=[('10%', 'Discount on any treatment'), ('£0', 'Emergency access fee'),
               ('Same day', 'Emergency appointment'), ('Worldwide', 'Injury & emergency cover'),
               ('£0', 'Referral fee')],
        link=('Fees and membership', H.rel('fees', depth))) + '</div>')

    blocks.append('<div id="visit">' + c_ed(
        H, depth, 'Find us', 'Come and say hello.',
        ['Holly Close, The Drift, Botesdale, Suffolk IP22 1DH — with on-site parking and '
         'step-free access throughout.',
         'New patients are very welcome. Send us a message or call the practice on '
         '<a class="link-inline" href="tel:%s">%s</a> and we will find you an appointment.'
         % (SITE['phone_href'], SITE['phone'])],
        link=('Get in touch', H.rel('contact', depth)),
        image='images/cards/practice-2.jpg', alt='Inside the practice') + '</div>')

    out.append('<div class="tab-scope">%s</div>' % ''.join(blocks))

    out.append(c_strip(H, depth, 'What we treat', 'Four areas of care.', [
        {'key': 'general', 'label': '01', 'title': 'General dentistry',
         'text': 'We are your trusted local family dental practice for all kinds of general '
                 'dentistry.', 'image': 'images/cards/general-dentistry.jpg',
         'alt': 'A dentist treating a patient'},
        {'key': 'cosmetic', 'label': '02', 'title': 'Cosmetic dentistry',
         'text': 'Treatments that enhance, align, and whiten or tone your teeth for a more '
                 'attractive appearance.', 'image': 'images/cards/cosmetic-dentistry.jpg',
         'alt': 'Cosmetic dental treatment'},
        {'key': 'preventative', 'label': '03', 'title': 'Preventative dentistry',
         'text': 'Routine dental appointments are essential to maintain good oral health and a '
                 'happy smile.', 'image': 'images/cards/preventative-dentistry.jpg',
         'alt': 'A healthy smile'},
        {'key': 'missing', 'label': '04', 'title': 'Missing teeth',
         'text': 'Crowns, bridges, dentures and implants — every option explained clearly '
                 'before you decide.', 'image': 'images/cards/implant-clinic-card.jpg',
         'alt': 'Implant consultation'},
    ], cols=4))

    out.append(c_quote(TESTIMONIALS))

    out.append(c_section(
        '<div class="section-head"><span class="label">Case studies</span>'
        '<h2>Real people, real problems, treated to the level patient allows us to treat them.</h2>'
        '<p>The cases on this page were published with consent and kind agreement of our happy '
        'patients.</p></div>'
        + c_cards(H, depth, [
            {'key': c['key'], 'label': c['label'], 'title': LABELS[c['key']],
             'text': _trim(c['teaser'], 150), 'image': c['thumb'], 'alt': LABELS[c['key']]}
            for c in CASES[:3]], cols=3)
        + '<div class="cluster u-mt-8">%s</div>'
          % c_btn('All case studies', H.rel('cases', depth), 'outline'),
        cls='section--paper-3'))

    out.append(c_statement(
        H, depth, 'Dental emergency?',
        'We do our best to provide same day emergency services.',
        'Same day emergency appointments for all our regular patients, and we will try our very '
        'best to accommodate others. Members of Our Plan pay no emergency access fee.',
        link=('Contact us now', H.rel('contact', depth))))
    return '\n'.join(out)


# ---- About -------------------------------------------------------------------
def r_about(depth, H):
    out = [c_page_head(
        H, depth, 'About the practice', 'About us',
        'Trusted, personalised care in a brand-new setting.',
        'images/heroes/about.jpg', c_crumbs(H, depth, [], 'About us'))]

    out.append(c_section('''<div class="home-intro__grid">
      <div>
        <p class="statement-text">We believe in dentistry that’s honest, ethical, and kind — where every patient is treated with the same care we’d want for our own family.</p>
        <div class="home-intro__body u-mt-6">
          <p>We take time to understand your concerns, respect your choices, and explain your options clearly — so you always feel informed, in control, and confident in your care.</p>
          <p>From your first visit to your final follow-up, our experienced and compassionate team is here to support you through every step of your dental journey. Whether you’re visiting for a routine check-up, advanced implant treatment, or a complete smile transformation, you’ll receive personalised care rooted in trust, transparency, and clinical excellence.</p>
          <p>Our goal is to help you achieve and maintain a healthy, beautiful smile for life.</p>
        </div>
      </div>
      <div class="home-intro__media">
        {ph}
      </div>
    </div>'''.format(ph=c_ph('The practice entrance sign'))))

    out.append(c_ed(
        H, depth, 'September 2024', 'A new smile in a purpose-built home.',
        ['We’re proud to welcome you to the new home of Botesdale Dental Practice &amp; Implant '
         'Clinic, now located in a purpose-built, state-of-the-art facility in the heart of '
         'Botesdale, Suffolk.',
         'Founded in 2010 by experienced dentist Dr Martin Sulo and managed alongside his wife '
         'Eve Sulo, our family-run clinic continues to offer the same trusted care — now with '
         'enhanced space, modern equipment, and cutting-edge facilities designed to support the '
         'best in patient care.',
         'Together with our dedicated professional team, we’ve created a warm, friendly '
         'environment that’s also fully accessible, thoughtfully designed, and equipped with the '
         'latest in dental technology.'],
        image='images/cards/practice-3.jpg', alt='Inside the new practice', rev=True))

    out.append(c_section('''<div class="section-head"><span class="label">Our mission</span>
      <h2>To deliver high-quality, evidence-based dentistry using the best tools, techniques, and materials available.</h2>
      <p>We stay ahead of the curve through ongoing professional development, working with leading labs, and investing in innovations that ensure patients receive expert, personalised care.</p></div>
      <div class="prose u-measure">
        <p>We offer a full range of services, including:</p>
        <ul>
          <li>Routine check-ups and hygiene care</li>
          <li>Same-day crowns, crafted on-site while you wait</li>
          <li>Cosmetic dentistry — from whitening to full smile makeovers</li>
          <li>Dental implants, surgical procedures, and bone regeneration procedures</li>
          <li>Family dentistry — gentle care for children, adults, and older patients</li>
        </ul>
        <p>Whether you’re a long-standing patient or visiting us for the first time, our new home was designed with you in mind — providing a relaxing space where care is not only clinical, but compassionate.</p>
      </div>
      <div class="u-mt-8">%s</div>''' % c_btn('Now welcoming new patients', H.rel('contact', depth), 'outline'),
      cls='section--paper-3'))

    out.append('''<section class="team">
  <div class="wrap section--tight">
    <div class="section-head">
      <span class="label">Our people</span>
      <h2>Meet our team</h2>
      <p>All our dentists adhere to the rules governing the profession under strict guidance from the
        <a class="link-inline" href="https://www.gdc-uk.org" rel="noopener">General Dental Council (GDC)</a>
        “Standards for Dental Professionals”.</p>
    </div>
  </div>
  <div class="team__row">
    <div class="team__media">{martin}</div>
    <div class="team__text">
      <h3>Dr Martin Sulo</h3>
      <span class="label">Dental Surgeon &middot; MUD Olomouc 1998</span>
      <p>I am proud to be a general dental practitioner, fortunate enough to focus on the aspects of dentistry I most enjoy. Together with my wife, Eve, we have owned Botesdale Dental Practice &amp; Implant Clinic since 2010. Over the years, despite many challenges, we have grown it into a modern and successful practice.</p>
      <p>My main areas of interest include dental implantology, crown and bridgework, composite restorations, and clear aligners.</p>
      <p>Outside of work, family comes first. I cherish time with my wife and our two wonderful boys — tennis, football, family travel, and our dog Nero, who ensures I get plenty of interesting walks every day.</p>
      <p class="team__gdc">GDC No: 84351</p>
    </div>
  </div>
  <div class="team__row team__row--rev">
    <div class="team__media">{eve}</div>
    <div class="team__text">
      <h3>Mrs Eve Sulo</h3>
      <span class="label">Practice Manager</span>
      <p>I began my career in 1995 as a trainee orthodontic nurse in Hong Kong, an experience that taught me a great deal at a young age and laid the foundation for becoming a Registered Dental Nurse here in the United Kingdom.</p>
      <p>Since then, I have gained a wealth of experience across many areas of dental healthcare within both the NHS and private sector. In my role, I ensure that our dedicated team has all the support and resources they need to provide the highest level of care to our patients.</p>
      <p>I am also available to discuss any aspect of our patients’ — or potential patients’ — dental healthcare and treatment. I pride myself on being approachable and genuinely enjoy my role within the practice.</p>
      <p class="team__gdc">GDC No: 105918</p>
    </div>
  </div>
</section>'''.format(martin=c_ph('Portrait — Dr Martin Sulo'),
                     eve=c_ph('Portrait — Mrs Eve Sulo')))

    out.append(c_process(H, depth, 'The practice', 'Practical details', [
        ('Purpose-built since 2024', 'A state-of-the-art facility in the heart of Botesdale, '
         'opened in September 2024.'),
        ('Fully accessible', 'Step-free access throughout, designed in from the start rather '
         'than retro-fitted.'),
        ('On-site parking', 'Off-street parking in the practice grounds.'),
        ('Same-day crowns', 'Crowns designed, milled and fitted on site while you wait.'),
        ('Working with leading labs', 'We collaborate with certified technicians across the UK '
         'and Europe who specialise in their respective fields.')]))

    out.append(c_cta(H, depth, 'Come and meet the team.',
                     'Now welcoming new patients — come and experience dentistry at its best.',
                     secondary=('Fees and membership', 'fees')))
    return '\n'.join(out)


# ---- Treatments hub ----------------------------------------------------------
def r_treatments(depth, H):
    out = [c_page_head(
        H, depth, 'Treatments', 'Every treatment starts with a conversation.',
        'Four areas of care, plus a dedicated implant clinic — all under one roof.',
        'images/heroes/general.jpg', c_crumbs(H, depth, [], 'Treatments'))]

    specs = [('general', 'Check-ups, fillings, root canal treatment, extractions, emergencies '
                         'and support for nervous patients.', False, False),
             ('cosmetic', 'Clear aligners, veneers, crowns, bridges, whitening and gum '
                          'reshaping.', True, True),
             ('preventative', 'Check-ups, hygiene visits and help with sensitive teeth — the '
                              'foundation of everything else.', False, False),
             ('missing', 'Crowns, bridges, dentures and implant-supported replacements.', True, True)]
    imgs = {'general': 'images/cards/general-dentistry.jpg',
            'cosmetic': 'images/cards/cosmetic-dentistry.jpg',
            'preventative': 'images/cards/preventative-dentistry.jpg',
            'missing': 'images/cards/implant-clinic-card.jpg'}
    for i, (k, text, rev, warm) in enumerate(specs, 1):
        out.append(c_ed(H, depth, '%02d — %s' % (i, LABELS[k]), CATEGORY[k]['lead'],
                        [text], link=('Learn more', H.rel(k, depth)),
                        image=imgs[k], alt=LABELS[k], rev=rev, warm=warm))

    out.append(c_statement(
        H, depth, '05 — Implant clinic',
        'A dedicated implant clinic, from consultation to aftercare.',
        'Dental implants offer a proven, long-lasting solution for bringing back your smile and '
        'restoring your ability to bite and chew comfortably — planned with 3D CBCT imaging and '
        'carried out here at the practice.',
        facts=[('3D', 'CBCT planning'), ('In-house', 'Placement & restoration'),
               ('Aftercare', 'Built into the plan')],
        link=('Visit the implant clinic', H.rel('implant', depth))))

    out.append(c_process(H, depth, 'First visit', 'What happens, in order', [
        ('Consultation', 'A conversation about what is bothering you, or what you would like to '
         'improve.'),
        ('Assessment', 'A full examination of teeth, gums, bite and soft tissues, with '
         'radiographs where they are needed.'),
        ('Options and costs', 'Every reasonable option written down, with a fully costed '
         'treatment plan.'),
        ('Treatment', 'Carried out in a sequence and at a pace that suits you.'),
        ('Review', 'A follow-up to make sure everything has settled, then back onto a '
         'preventative recall.')]))

    out.append(c_cta(H, depth, 'Ready when you are.', secondary=('Fees and membership', 'fees')))
    return '\n'.join(out)


# ---- Implant clinic ----------------------------------------------------------
def r_implant(depth, H):
    out = [c_page_head(
        H, depth, 'Implant clinic', 'Implant clinic',
        'A proven, long-lasting way to replace missing or failing teeth.',
        'images/heroes/implant-clinic.jpg', c_crumbs(H, depth, [], 'Implant clinic'))]

    out.append(c_section('''<div class="with-rail">
      <div class="prose">
        <p class="statement-text statement-text--wide">Struggling with missing or failing teeth? Or have you lost some of your own natural teeth over time? Thanks to advances in modern dentistry, you no longer need to depend solely on bridges or dentures.</p>
        <p>Dental implants offer a proven, long-lasting solution for bringing back your smile and restoring your ability to bite and chew comfortably. Here’s how they work:</p>
        <ol>
          <li>A dental implant is a small titanium screw placed in the jaw to act like a natural tooth root.</li>
          <li>Once it bonds with the bone, a beautifully crafted crown, bridge or denture is fixed to the implant for a stable, natural finish.</li>
          <li>The result looks, feels and functions like your own teeth — and is cared for in exactly the same way.</li>
        </ol>
        <h2>Life benefits</h2>
        <ul>
          <li>When you lose your natural teeth, your jaw bone and surrounding tissues start to resorb over time. When implants are placed in the jaw, it stimulates the remaining bone to grow and mesh around the metal, along with tiny blood vessels, preventing bone loss.</li>
          <li>Retained bone structure prevents the face from acquiring a ‘sunken’ look.</li>
          <li>Implants help restore function so you can eat, chew and bite as usual.</li>
          <li>Implants are a natural-looking way to replace missing teeth.</li>
        </ul>
      </div>
      <aside class="rail">
        <span class="label">Implant clinic</span>
        <nav class="rail__list">
          <a href="{implant}" class="is-active">Implant clinic</a>
          <a href="{ir}">Implant referrals</a>
          <a href="{missing}">Missing teeth</a>
          <a href="{cases}">Case studies</a>
          <a href="{fees}">Fees and membership</a>
        </nav>
        <div class="notice u-mt-8">
          <strong>Referring a patient?</strong>
          We accept implant referrals from patients and dental professionals alike, with a £0 referral fee for members of Our Plan.
        </div>
      </aside>
    </div>'''.format(implant=H.rel('implant', depth), ir=H.rel('implant-referrals', depth),
                     missing=H.rel('missing', depth), cases=H.rel('cases', depth),
                     fees=H.rel('fees', depth))))

    out.append(c_process(H, depth, 'The pathway', 'From consultation to aftercare', [
        ('Consultation and assessment', 'A full examination and a discussion of what you want to '
         'achieve, including whether an implant is the right answer at all.'),
        ('3D CBCT imaging', 'A three-dimensional scan shows the bone volume, its quality and the '
         'position of the nerve and sinus — planning is done on real anatomy, not guesswork.'),
        ('Written treatment plan', 'Every stage, every visit and every cost, in writing, before '
         'anything begins.'),
        ('Placement', 'The implant is placed under local anaesthetic. Most patients are '
         'surprised by how straightforward the appointment is.'),
        ('Integration', 'The bone bonds to the implant over roughly three to six months. A '
         'temporary tooth is provided where appearance matters.'),
        ('The final restoration', 'A crown, bridge or denture is crafted and fitted to the '
         'implant.'),
        ('Aftercare', 'Implants need cleaning and monitoring like natural teeth. Reviews are '
         'built into the plan.')]))

    out.append(c_section(
        '<div class="section-head"><span class="label">Common questions</span>'
        '<h2>Dental implants, answered</h2></div>' + c_accordion([
          ('Am I suitable for dental implants?',
           '<p>Most adults are. What matters is the volume and quality of bone, healthy gums, and '
           'general health — smoking and uncontrolled diabetes both affect healing. A CBCT scan '
           'answers the question properly.</p>'),
          ('Is it painful?',
           '<p>Placement is carried out under local anaesthetic and most patients report it is '
           'more comfortable than an extraction. Expect some tenderness for a few days '
           'afterwards.</p>'),
          ('How long do implants last?',
           '<p>Implants have a long clinical track record, and with good hygiene and regular '
           'maintenance many last decades. The restoration on top may need replacing sooner than '
           'the implant itself.</p>'),
          ('What if there is not enough bone?',
           '<p>Bone regeneration procedures are carried out here at the practice and can rebuild '
           'the site so that an implant becomes possible.</p>'),
          ('How much do implants cost?',
           '<p>Cost depends on the number of implants and the restoration on top. You will '
           'receive a fully costed written plan after your assessment, and finance options are '
           'available — see <a class="link-inline" href="fees-and-membership.html">fees and '
           'membership</a>.</p>'),
        ], idbase='implant'), cls='section--paper-3'))

    out.append(c_quote([TESTIMONIALS[0]]))
    out.append(c_cta(H, depth, 'Would you like to talk about dental implants?',
                     'Get in touch and we will arrange a consultation.',
                     primary=('Book a consultation', 'contact'),
                     secondary=('Implant referrals', 'implant-referrals'), dark=True))
    return '\n'.join(out)


# ---- Implant referrals -------------------------------------------------------
def r_implant_referrals(depth, H):
    out = [c_page_head(
        H, depth, 'Implant clinic', 'Implant referrals',
        'Self-referrals from patients and referrals from dental professionals.',
        'images/heroes/implant-referrals.jpg',
        c_crumbs(H, depth, ['implant'], 'Implant referrals'))]

    patient_fields = [
        f_step('Your details', [
            f_field('psr-name', 'Full name', required=True),
            f_field('psr-dob', 'Date of birth', 'date'),
            f_field('psr-address', 'Address', 'textarea', rows=3),
            f_field('psr-postcode', 'Postcode'),
            f_field('psr-phone', 'Phone', 'tel', required=True),
            f_field('psr-email', 'Email', 'email', required=True),
        ]),
        f_step('Your health', [
            f_field('psr-medical', 'Please provide any relevant medical history (including medications)',
                    'textarea', rows=4),
            f_field('psr-dental', 'Please describe any recent dental issues, treatments, or concerns',
                    'textarea', rows=4),
        ], intro='Both of these are optional here — we will go through your history properly at '
                 'your assessment. Anything you can tell us now helps us prepare.'),
        f_step('What you are looking for', [
            f_field('psr-reason', 'What would you like to improve or restore with dental implants?',
                    'textarea', rows=4),
            f_field('psr-when', 'How soon are you hoping to start?', 'select',
                    options=['As soon as possible', 'Within 3 months', 'Within 6 months',
                             'Just exploring options']),
            f_field('psr-contact', 'Preferred contact method', 'select',
                    options=['Phone', 'Email', 'Either']),
        ]),
    ]

    pro_fields = [
        f_step('Your details', [
            f_field('dpr-name', 'Name', required=True),
            f_field('dpr-practice', 'Practice / organisation', required=True),
            f_field('dpr-gdc', 'GDC / professional number', required=True),
            f_field('dpr-address', 'Address', 'textarea', rows=3),
            f_field('dpr-postcode', 'Postcode'),
            f_field('dpr-phone', 'Phone', 'tel', required=True),
            f_field('dpr-email', 'Email', 'email', required=True),
        ]),
        f_step('Patient details', [
            f_field('dpr-pname', 'Full name', required=True),
            f_field('dpr-pdob', 'Date of birth', 'date'),
            f_field('dpr-paddress', 'Address', 'textarea', rows=3),
            f_field('dpr-ppostcode', 'Postcode'),
            f_field('dpr-pphone', 'Phone', 'tel'),
            f_field('dpr-pemail', 'Email', 'email'),
        ]),
        f_step('Referral details', [
            f_field('dpr-reason', 'Reason for referral', 'textarea', rows=4, required=True),
            f_field('dpr-history', 'Relevant medical and dental history', 'textarea', rows=4),
            f_checks('dpr-scope', 'Referral scope',
                     ['Assessment only', 'Assessment and treatment', 'Surgical placement only',
                      'Restorative only', 'Second opinion']),
            f_field('dpr-notes', 'Any other notes', 'textarea', rows=3),
        ]),
    ]

    out.append(c_section(f_chooser('implant', [
        ('patient', 'I am a patient', 'Refer yourself for an implant assessment',
         'Patient self referral',
         '<p class="lead u-mb-8">Not registered with us? You can refer yourself directly. '
         'Complete the form and we will contact you to arrange an assessment.</p>'
         + f_form('patientSelfReferral', patient_fields, 'Send referral', steps=True,
                  note='We will contact you to arrange an assessment appointment. Please do not '
                       'include confidential clinical detail you would rather send by post.',
                  success_title='Referral received.',
                  success_text='Thank you — we will be in touch to arrange your assessment.')),
        ('professional', 'I am a dental professional', 'Refer a patient to the implant clinic',
         'Dental professionals referral',
         '<p class="lead u-mb-8">We welcome implant referrals from colleagues. Patients are '
         'assessed and treated here, with updates shared back to the referring practice '
         'throughout.</p>'
         + f_form('professionalReferral', pro_fields, 'Send referral', steps=True,
                  note='Radiographs and clinical images can be emailed separately to '
                       'reception@botesdaledental.co.uk.',
                  success_title='Referral received.',
                  success_text='Thank you. We will confirm receipt and contact the patient '
                               'directly to arrange an assessment.')),
    ])))

    out.append(c_process(H, depth, 'Shared care', 'How a referral works', [
        ('Referral received', 'We acknowledge every referral and confirm what we have been '
         'sent.'),
        ('Assessment', 'The patient is seen for a full implant assessment including CBCT imaging '
         'where indicated.'),
        ('Written plan', 'A treatment plan and costing goes to the patient, with a copy to the '
         'referring practice.'),
        ('Treatment', 'Carried out here at Botesdale, with the referring dentist kept informed '
         'throughout.'),
        ('Return to your practice', 'Once treatment is complete, routine care returns to the '
         'referring dentist.')]))

    out.append(c_cta(H, depth, 'Questions about a referral?',
                     'Call the practice on %s and ask for Dr Martin Sulo.' % SITE['phone'],
                     primary=('Contact us', 'contact'),
                     secondary=('CBCT & OPG referrals', 'referrals')))
    return '\n'.join(out)


# ---- Referrals (CBCT / OPG) --------------------------------------------------
def r_referrals(depth, H):
    out = [c_page_head(
        H, depth, 'For professional colleagues', 'Referrals',
        'A reliable and efficient CBCT and OPG referral service.',
        'images/heroes/referrals.jpg', c_crumbs(H, depth, [], 'Referrals'))]

    out.append(c_ed(
        H, depth, 'Imaging service',
        'We are pleased to offer a reliable and efficient CBCT and OPG referral service for our '
        'professional colleagues.',
        ['We provide high-quality imaging using the latest dental radiographic technology, '
         'ensuring accurate diagnostics and seamless collaboration.',
         'Our dedicated team is committed to delivering clear, precise scans with fast '
         'turnaround times, enabling you to plan and treat with confidence. We accept referrals '
         'from all dental professionals and guarantee a welcoming, professional experience for '
         'every patient you entrust to us.',
         'Whether you require <strong>3D CBCT imaging</strong> for complex diagnostics or '
         '<strong>OPG radiographs</strong> for routine assessment, we are here to support your '
         'clinical needs with excellence and efficiency.'],
        image='images/cards/cbct-imaging.jpg', alt='CBCT imaging at the practice'))

    ref_fields = [
        f_step('Referring dentist', [
            f_field('ref-name', 'Name', required=True),
            f_field('ref-gdc', 'GDC number', required=True),
            f_field('ref-practice', 'Practice name', required=True),
            f_field('ref-address', 'Practice address', 'textarea', rows=3),
            f_field('ref-email', 'Email', 'email', required=True),
            f_field('ref-phone', 'Phone', 'tel', required=True),
        ]),
        f_step('Patient details', [
            f_field('ref-pname', 'Full name', required=True),
            f_field('ref-pdob', 'Date of birth', 'date', required=True),
            f_field('ref-paddress', 'Address', 'textarea', rows=3),
            f_field('ref-pphone', 'Phone', 'tel', required=True),
            f_field('ref-pemail', 'Email (optional)', 'email'),
        ]),
        f_step('Clinical information', [
            f_field('ref-reason', 'Reason for CBCT referral', 'textarea', rows=3, required=True),
            f_field('ref-history', 'Relevant medical history', 'textarea', rows=3),
            f_checks('ref-area', 'Area of interest (tick all that apply)',
                     ['Upper right quadrant', 'Upper left quadrant', 'Lower right quadrant',
                      'Lower left quadrant', 'Maxilla', 'Mandible', 'TMJ', 'Other']),
            f_field('ref-other', 'If ‘other’, please give details', 'textarea', rows=2),
        ]),
        f_step('Imaging and reporting', [
            f_field('ref-fov', 'Scan type requested', 'select', required=True,
                    options=['Small field of view (FOV)', 'Medium field of view (FOV)',
                             'Large field of view (FOV)', 'OPG radiograph']),
            f_field('ref-res', 'Resolution', 'select',
                    options=['Standard resolution', 'High resolution (where clinically justified)']),
            f_field('ref-notes', 'Specific notes / instructions', 'textarea', rows=3),
            f_field('ref-report', 'Radiology report', 'select', required=True,
                    options=['Full radiology report required (additional fee required)',
                             'Report by referring clinician']),
            f_field('ref-concerns', 'If a report is required, please specify any particular '
                                    'concerns or regions of interest', 'textarea', rows=3),
        ]),
    ]

    def sla_referrer(i):
        """One entitled person. Called for item 0 and for the clone template,
        so the two are identical by construction."""
        return [
            f_field('sla-referrer-%s-name' % i, 'Name', required=True,
                    name='sla-referrer[%s][name]' % i),
            f_field('sla-referrer-%s-gdc' % i, 'GDC/GMC registration number', required=True,
                    name='sla-referrer[%s][gdc]' % i),
            f_field('sla-referrer-%s-role' % i, 'IRMER 2017 role', 'select', required=True,
                    name='sla-referrer[%s][role]' % i,
                    options=['Referrer', 'Operating (reporting)', 'Both']),
        ]

    sla_fields = [
        f_step('Referring practice', [
            f_field('sla-practice', 'Practice name', required=True),
            f_field('sla-address', 'Practice address', 'textarea', rows=3),
            f_field('sla-phone', 'Phone', 'tel', required=True),
            f_field('sla-email', 'Email', 'email', required=True),
            f_field('sla-employer', 'Name of employer', required=True),
        ]),
        f_step('Entitled people', [
            f_repeat('sla-referrer', 'Person', sla_referrer, min_items=1, max_items=12,
                     add_label='Add another person'),
        ], intro='List everyone at the referring practice who will refer patients for '
                 'radiographic examinations and/or report on dental images. Add as many as you '
                 'need. Evidence of suitable training must be provided for each of them.'),
        f_step('Confirm and sign', [
            # The criteria have to sit here, next to the box that agrees to them.
            # They used to be above the form, which the wizard put on a different
            # screen — leaving the checkbox pointing at something not on the page.
            '<div class="notice notice--plain"><strong>Referral criteria</strong>'
            'This document will be used by both parties as the basis for the referral of patients '
            'and the justification/authorisation of dental radiographic examinations.</div>',
            '<div class="field"><label class="choice">'
            '<input type="checkbox" id="sla-agree" name="sla-agree" required>'
            '<span>We agree: (1) To use the referral criteria set out above; (2) That evidence of '
            'adequate training has been provided for each of the people named in this form, '
            'appropriate to their IR(ME)R 2017 roles; (3) That adequate information will accompany '
            'each referred patient to allow the justification process to proceed.</span></label>'
            '<span class="field__error" role="alert"></span></div>',
            f_field('sla-signame', 'Your name', required=True,
                    hint='Signing on behalf of the practice.'),
            f_field('sla-date', 'Date', 'date', required=True),
        ], intro='Someone able to sign for the practice should complete this step.'),
    ]

    out.append(c_section('''<div class="notice u-mb-8">
      <strong>These forms are for dental practices, not patients</strong>
      If you are a patient looking for a scan, your own dentist refers you to us — please ask them. To enquire about implant treatment for yourself, use the <a class="link-inline" href="implant-referrals.html#patient">implant self-referral form</a>.
    </div>
    <div class="form-stack">
      <div class="form-block">
        <h2 class="u-mb-6">Send a referral</h2>
        <p class="lead u-mb-8 u-measure">Use this for every patient you refer to us for a CBCT scan or an OPG radiograph.</p>
        {f1}
      </div>
      <div class="form-block">
        <h2 class="u-mb-4">Register your practice</h2>
        <p class="label u-mb-6">One-off · first referral only</p>
        <div class="u-mb-8 u-measure">
          <p class="lead">Before we can accept referrals from your practice, we need to record who there is entitled to refer patients for X-rays and to report on the images. The radiation regulations (IR(ME)R 2017) require us both to keep that on file. You may know it as the <strong>service level agreement</strong>.</p>
          <p class="u-mt-4"><strong>Fill in the form below</strong> the first time you refer a patient to us. It takes a couple of minutes, and you will not need to do it again unless the people at your practice change.</p>
        </div>
        {f2}
        <div class="u-mt-8 u-measure">
          <h3 class="u-mb-4">Who you are referring to</h3>
          {specs}
        </div>
      </div>
    </div>'''.format(
        f1=f_form('cbctReferral', ref_fields, 'Send referral', steps=True,
                  note='Please do not email patient-identifiable images to a personal address. '
                       'Contact the practice if you need a secure transfer.',
                  success_title='Referral received.',
                  success_text='Thank you. We will contact the patient to arrange their scan and '
                               'confirm with your practice.'),
        f2=f_form('slaForm', sla_fields, 'Register practice', steps=True,
                  note='You only need to do this once. We will confirm by email when your '
                       'practice is registered.',
                  success_title='Practice registered.',
                  success_text='Thank you — we will confirm by email and keep this on file. '
                               'Future referrals can be sent on their own.'),
        specs=c_specs([
            ('Practice', 'Botesdale Dental Practice &amp; Implant Clinic'),
            ('Address', 'The Drift, Botesdale, Suffolk IP22 1DH'),
            ('Phone', '<a href="tel:%s">%s</a>' % (SITE['phone_href'], SITE['phone'])),
            ('Email', '<a href="mailto:%s">%s</a>' % (SITE['email'], SITE['email'])),
            ('Clinical lead', 'Dr Martin Sulo')]))))

    out.append(c_cta(H, depth, 'Referring for implants instead?',
                     'We accept implant referrals from patients and dental professionals alike.',
                     primary=('Implant referrals', 'implant-referrals'),
                     secondary=('Contact the practice', 'contact')))
    return '\n'.join(out)


# ---- Fees and membership -----------------------------------------------------
def r_fees(depth, H):
    out = [c_page_head(
        H, depth, 'Fees and membership', 'Fees and membership',
        'Regular care at a price you can plan for.',
        'images/heroes/fees.jpg', c_crumbs(H, depth, [], 'Fees and membership'))]

    out.append(c_section('''<div class="cols-2 grid--loose">
      <div>
        <span class="label">What it costs</span>
        <h2 class="u-mt-4 u-mb-6">We offer you a range of options when it comes to paying for your treatment.</h2>
        <div class="prose">
          <ul>
            <li>We accept cash, credit and debit cards.</li>
            <li>We have a Membership Scheme, which is from £19.95 per month and provides many benefits including worldwide cover for dental emergencies whilst on holiday, out of hours emergency care and advice 365 days of the year when you are at home, and a 10% saving on the cost of many dental treatments.</li>
            <li>We ask for payment for treatment as the treatment progresses, allowing you to stagger and organise your treatment and appointments to suit your budget and time scales.</li>
          </ul>
          <p>Please be aware that the prices below are a guide only. We really do try to give a good idea, but we don’t waste your time — treatment for each patient is tailored to suit the needs and choices of the individual. Specific treatments vary on different patients and our fees reflect this.</p>
          <p>We always prepare written treatment plans and proposals and a clear outline of the fees involved for our complex cases.</p>
        </div>
      </div>
      <div>
        <span class="label">Membership scheme</span>
        <h2 class="u-mt-4 u-mb-6">Our Plan</h2>
        <div class="cols-2 grid--tight u-mb-8">
          <div class="plan plan--feature">
            <span class="label">Peace of mind for</span>
            <h3>Adults</h3>
            <div class="plan__price">£19.95<small> / month</small></div>
          </div>
          <div class="plan">
            <span class="label">Peace of mind for</span>
            <h3>Children</h3>
            <div class="plan__price">£8.40<small>* / month</small></div>
          </div>
        </div>
        <p class="meta u-mb-8">*Child must have at least one adult who is part of our membership plan.</p>
        <h3 class="u-mb-4">Your benefits include the following:</h3>
        <ul class="plan__list">
          <li>Two visits a year with your dentist for a full oral health assessment.</li>
          <li>Two visits a year with your dentist for assessment and maintenance to ensure the ultimate in dental hygiene.</li>
          <li>10% off any treatment — cannot be claimed retrospectively.</li>
          <li>All necessary X-rays.</li>
          <li>£0 emergency access appointment outside of recall intervals.</li>
          <li>£0 referral fee.</li>
          <li>Preventative and dietary advice.</li>
          <li>Emergency service 365 days of the year should you require advice or treatment when the practice is closed.</li>
          <li>UK and worldwide dental injury and emergency insurance available.</li>
        </ul>
      </div>
    </div>'''))

    out.append(c_section('''<div class="cols-2 grid--loose">
      <div>
        <span class="label">Price guide</span>
        <h2 class="u-mt-4 u-mb-6">Botesdale Dental Practice and Implant Clinic price guide</h2>
        <p class="meta u-mb-6">Fees correct as of February 2022. A new price list will be provided soon and we will send an information pack to every new patient.</p>
        <h3 class="u-mb-4">Our Plan</h3>
        <div class="price-list">
          <div class="price-list__row"><div><strong>2 exams &amp; oral health visits</strong><div class="price-list__note">With small X-rays</div></div><div>£19.95 / month</div></div>
          <div class="price-list__row"><div><strong>3 exams &amp; oral health visits</strong><div class="price-list__note">With small X-rays</div></div><div>£26.25 / month</div></div>
          <div class="price-list__row"><div><strong>4 exams &amp; oral health visits</strong><div class="price-list__note">With small X-rays</div></div><div>£32.55 / month</div></div>
        </div>
        <div class="notice u-mt-8">
          <strong>Private fees are for guidance only</strong>
          A fully costed treatment plan will be provided to you at your appointment.
        </div>
        <h3 class="u-mt-8 u-mb-4">Finance</h3>
        <p class="muted">Payment plans are available for dental treatment. Please ask during your next visit for more details.</p>
      </div>
      <div>
        <span class="label">What is your investment?</span>
        <h2 class="u-mt-4 u-mb-6">£19.95 per month — that’s it.</h2>
        <p class="lead u-mb-8">No frills or hidden extras. So, for just £19.95 per month, we will help you create and maintain a confident smile.</p>
        {tcs}
        <div class="u-mt-8">{cta}</div>
      </div>
    </div>'''.format(
        tcs=c_accordion([
            ('Terms and conditions',
             '<ul><li>Minimum initial term of 12 months in the membership plan. If you cancel we '
             'will invoice you for any discount given.</li>'
             '<li>One month’s notice to cancel thereafter.</li>'
             '<li>Children must have at least one adult who is part of our membership plan.</li>'
             '</ul>'),
            ('How do I join?',
             '<p>You will need an initial assessment so that we can be sure your mouth is '
             'dentally fit before the plan starts. Speak to Eve at reception, or '
             '<a class="link-inline" href="contact-us.html">send us a message</a> and we will '
             'call you back.</p>'),
            ('What is not included?',
             '<p>The plan covers your routine preventative care. Restorative and cosmetic '
             'treatment is charged separately, with a 10% member discount applied.</p>'),
        ], idbase='fees'),
        cta=c_btn('Book a consultation', H.rel('contact', depth), 'solid')),
        cls='section--paper-3'))

    out.append(c_statement(
        H, depth, 'What to do next?',
        'Would you like to discuss our membership scheme?',
        'Please get in touch — we will explain exactly what is included and what your treatment '
        'would cost before you commit to anything.',
        link=('Contact the practice', H.rel('contact', depth))))
    return '\n'.join(out)


# ---- Case studies index ------------------------------------------------------
def r_cases(depth, H):
    out = [c_page_head(
        H, depth, 'Case studies', 'Case studies',
        'Real people with real problems, treated to the level the patient allows us to treat them.',
        'images/heroes/case-studies.jpg', c_crumbs(H, depth, [], 'Case studies'))]

    out.append(c_section('''<div class="cols-2 grid--loose">
      <div class="prose">
        <p class="statement-text statement-text--wide">We treat real people with real problems to the level patient allows us to treat them.</p>
        <p>The cases on this page were published with consent and kind agreement of our happy patients.</p>
        <p>We acknowledge that these cases may not be perfect, but just like everything in life is not ideal or perfect, neither are our teeth.</p>
        <p>We work with a range of dental laboratories across the UK and Europe, enabling us to collaborate with certified highly skilled technicians who specialise in their respective fields.</p>
      </div>
      <div>{quote}</div>
    </div>'''.format(quote='<div class="notice"><strong>What our patients say</strong>'
                           '&ldquo;%s&rdquo;<div class="u-mt-4 label">%s</div></div>'
                           % (_e(TESTIMONIALS[1][0]), _e(TESTIMONIALS[1][1])))))

    items = [{'key': c['key'], 'label': c['label'], 'title': LABELS[c['key']],
              'text': c['teaser'], 'image': c['thumb'], 'alt': LABELS[c['key']]} for c in CASES]
    out.append('<h2 class="visually-hidden">Our case studies</h2>')
    out.append(c_strip(H, depth, '', '', items, cols=3))

    out.append(c_cta(H, depth, 'Could we help with something similar?',
                     'Every mouth is different. Book an assessment and we will tell you honestly '
                     'what is possible.', secondary=('Implant clinic', 'implant')))
    return '\n'.join(out)


# ---- Case study detail -------------------------------------------------------
def r_case(key, depth, H):
    c = CASE_BY_KEY[key]
    idx = [x['key'] for x in CASES].index(key)
    prev = CASES[idx - 1]['key'] if idx > 0 else None
    nxt = CASES[idx + 1]['key'] if idx < len(CASES) - 1 else None

    out = [c_page_head(
        H, depth, 'Case study', LABELS[key], '',
        'images/heroes/case-studies.jpg', c_crumbs(H, depth, ['cases'], LABELS[key]))]

    body = []
    for kind, val in c['body']:
        if kind == 'h2':
            body.append('<h2>%s</h2>' % _e(val))
        elif kind == 'p':
            body.append('<p>%s</p>' % val)
        elif kind == 'ul':
            body.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % _e(i) for i in val))

    out.append(c_section(
        '<div class="with-rail"><div class="case-body prose">'
        '<div class="case-meta"><span class="badge badge--accent">%s</span></div>'
        '%s</div>%s</div>' % (_e(c['label']), ''.join(body), c_rail(H, depth, key, 'cases'))))

    out.append(c_section(
        '<div class="section-head"><span class="label">The case</span><h2>Before, during and after</h2>'
        '<p>Click any image to view it larger.</p></div>' + c_gallery(H, depth, c['shots']),
        cls='section--paper-3'))

    out.append('<div class="wrap section--tight case-consent"><p class="meta">These images are '
               'published with the consent and kind agreement of our patient. Individual results '
               'vary — the right treatment for you will depend on your own clinical '
               'situation.</p></div>')

    out.append(c_pager(H, depth, prev, nxt))
    out.append(c_cta(H, depth, 'Ready when you are.',
                     secondary=('All case studies', 'cases')))
    return '\n'.join(out)


# ---- Contact -----------------------------------------------------------------
def r_contact(depth, H):
    out = [c_page_head(
        H, depth, 'Get in touch', 'Contact us',
        'To register as a new patient or to contact us for any other reason, please use the form '
        'or give us a call. We welcome all enquiries.',
        'images/heroes/contact.jpg', c_crumbs(H, depth, [], 'Contact us'))]

    fields = [
        f_field('c-name', 'Your name', required=True),
        f_field('c-email', 'Your email', 'email', required=True),
        f_field('c-phone', 'Phone', 'tel', required=True),
        f_field('c-reason', 'What is it about?', 'select', options=[
            'Registering as a new patient', 'Booking an appointment', 'Dental emergency',
            'Membership and fees', 'Implant enquiry', 'Referral enquiry', 'Something else']),
        f_field('c-message', 'Your message (optional)', 'textarea', full=True, rows=5),
        '<div class="field field--full"><label class="choice">'
        '<input type="checkbox" id="c-consent" name="c-consent" required>'
        '<span>I am happy for the practice to contact me about this enquiry. See our '
        '<a class="link-inline" href="privacy-policy.html">Privacy Policy</a>.</span></label>'
        '<span class="field__error" role="alert"></span></div>',
    ]

    hours = ''.join('<div class="spec"><span class="spec__k">%s</span>'
                    '<span class="spec__v">%s</span></div>' % (d, h) for d, h in SITE['hours'])

    out.append(c_section('''<div class="contact-grid">
      <div>
        <h2 class="u-mb-6">Send us a message</h2>
        {form}
      </div>
      <aside class="contact-aside">
        <div>
          <span class="label">Where to find us</span>
          <address class="u-mt-4 lead">
            Botesdale Dental Practice &amp; Implant Clinic<br>
            Holly Close<br>The Drift<br>Botesdale<br>Suffolk IP22 1DH
          </address>
        </div>
        <div>
          <span class="label">Opening hours</span>
          <div class="specs u-mt-4">{hours}</div>
        </div>
        <div>
          <span class="label">Get in touch</span>
          <div class="specs u-mt-4">
            <div class="spec"><span class="spec__k">Phone</span><span class="spec__v"><a href="tel:{tel_href}">{tel}</a></span></div>
            <div class="spec"><span class="spec__k">Email</span><span class="spec__v"><a href="mailto:{email}">{email}</a></span></div>
            <div class="spec"><span class="spec__k">Parking</span><span class="spec__v">On site, step-free</span></div>
          </div>
        </div>
        <div class="notice">
          <strong>Dental emergency?</strong>
          Please call the practice on <a href="tel:{tel_href}">{tel}</a> as early in the day as you can rather than using this form.
        </div>
      </aside>
    </div>'''.format(
        form=f_form('contactForm', fields, 'Send message',
                    note='We aim to reply within one working day. For anything urgent, please '
                         'call the practice.',
                    success_title='Thank you — your message has been sent.',
                    success_text='A member of the practice team will be in touch shortly.'),
        hours=hours, tel=SITE['phone'], tel_href=SITE['phone_href'], email=SITE['email'])))

    out.append(c_section('''<div class="section-head"><span class="label">How to find us</span>
      <h2>Holly Close, The Drift, Botesdale</h2></div>
      <div class="map">
        <iframe title="Map showing Botesdale Dental Practice &amp; Implant Clinic"
          src="https://www.google.com/maps?q=Botesdale+Dental+Practice+%26+Implant+Clinic,+The+Drift,+Botesdale,+IP22+1DH&output=embed"
          loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>''', cls='section--paper-3'))
    return '\n'.join(out)


# ---- Legal -------------------------------------------------------------------
def r_privacy(depth, H):
    out = [c_page_head(
        H, depth, 'Legal', 'Privacy Policy', '', 'images/heroes/privacy.jpg',
        c_crumbs(H, depth, [], 'Privacy Policy'), short=True)]
    out.append('''<section class="legal"><div class="wrap">
  <p class="legal__updated">Last updated 15 May 2026 &middot; Effective 15 May 2026</p>
  <div class="prose">
    <p>This Privacy Policy describes the policies of Botesdale Dental Practice &amp; Implant Clinic, Holly Close, The Drift, Botesdale, Suffolk IP22 1DH, United Kingdom of Great Britain and Northern Ireland; email: <a href="mailto:reception@botesdaledental.co.uk">reception@botesdaledental.co.uk</a>; phone: <a href="tel:+441379897176">01379 897176</a>, on the collection, use and disclosure of your information that we collect when you use our website (<a href="https://botesdaledental.co.uk">https://botesdaledental.co.uk</a>) (the “Service”). By accessing or using the Service, you are consenting to the collection, use and disclosure of your information in accordance with this Privacy Policy. If you do not consent to the same, please do not access or use the Service.</p>
    <p>We may modify this Privacy Policy at any time without any prior notice to you and will post the revised Policy on the Service. The revised Policy will be effective 180 days from when the revised Policy is posted on the Service, and your continued access or use of the Service after such time will constitute your acceptance of the revised Privacy Policy. We therefore recommend that you periodically review this page.</p>

    <h2>1. Information we collect</h2>
    <p>We will collect and process the following personal information about you:</p>
    <ul><li>Name</li><li>Email</li><li>Mobile or telephone number</li><li>Any information you choose to include in your message</li></ul>

    <h2>2. How we use your information</h2>
    <p>We will use the information that we collect about you for the following purposes:</p>
    <ul>
      <li>Responding to your enquiry and arranging appointments</li>
      <li>Providing and managing your dental care</li>
      <li>Meeting our legal, regulatory and professional obligations</li>
      <li>Managing customer support and administration of the practice</li>
    </ul>
    <p>If we want to use your information for any other purpose, we will ask you for consent and will use your information only on receiving your consent, and then only for the purpose(s) for which consent is granted, unless we are required to do otherwise by law.</p>

    <h2>3. How we share your information</h2>
    <p>We will not transfer your personal information to any third party without seeking your consent, except where this is necessary for your care (for example, a dental laboratory, a specialist to whom you are referred, or your own dentist where you have been referred to us), or where we are required to do so by law.</p>
    <p>We do not sell your personal information, and we do not share it with third parties for their own marketing purposes.</p>

    <h2>4. Retention of your information</h2>
    <p>We will retain your personal information with us for as long as we need it to fulfil the purposes for which it was collected, or as required to comply with our legal obligations. Dental records are retained in line with current NHS and professional record-retention guidance.</p>

    <h2>5. Your rights</h2>
    <p>Depending on the law that applies, you may have the right to access, rectify or erase your personal data, receive a copy of your personal data, restrict or object to the processing of your information, and — where we have collected and processed your information with your consent — withdraw that consent at any time.</p>
    <p>To exercise any of these rights, please write to us at <a href="mailto:reception@botesdaledental.co.uk">reception@botesdaledental.co.uk</a>. We will respond to your request in accordance with applicable law. Withdrawing consent will not affect the lawfulness of processing based on consent before its withdrawal.</p>

    <h2>6. Cookies</h2>
    <p>For details of how this website uses cookies, please see our <a href="cookie-policy.html">Cookie Policy</a>.</p>

    <h2>7. Security</h2>
    <p>The security of your information is important to us. We take reasonable security measures to protect it from unauthorised access, alteration or destruction. However, no method of transmission over the internet or method of electronic storage is completely secure, and we cannot guarantee absolute security.</p>

    <h2>8. Grievance / data protection officer</h2>
    <p>If you have any queries or concerns about the processing of your information, please contact the Practice Manager at Botesdale Dental Practice &amp; Implant Clinic, Holly Close, The Drift, Botesdale, Suffolk IP22 1DH, or email <a href="mailto:reception@botesdaledental.co.uk">reception@botesdaledental.co.uk</a>. We will address your concerns in accordance with applicable law.</p>
    <p>You also have the right to lodge a complaint with the Information Commissioner’s Office (ICO) at <a href="https://ico.org.uk" rel="noopener">ico.org.uk</a>.</p>
  </div>
</div></section>''')
    return '\n'.join(out)


def r_cookies(depth, H):
    rows = [
        ('Essential', [
            ('cookieyes-consent', 'Stores your cookie preferences so you are not asked again on every visit.', '1 year'),
            ('PHPSESSID', 'Preserves your session state across page requests.', 'Session'),
            ('bdp-cookie-choice', 'Records whether you accepted all cookies or essential cookies only.', '1 year'),
        ]),
        ('Analytics', [
            ('_ga', 'Registers a unique ID used to generate statistical data on how you use the website.', '1 year 1 month'),
            ('_ga_*', 'Used by Google Analytics to persist session state.', '1 year 1 month'),
        ]),
        ('Functional', [
            ('Google Maps', 'Loaded on the contact page to display our location. Google may set its own cookies.', 'Varies'),
            ('Google Fonts', 'Used to load the typefaces this site is set in.', 'Varies'),
        ]),
    ]
    tables = []
    for group, items in rows:
        body = ''.join('<tr><td><code>%s</code></td><td>%s</td><td>%s</td></tr>'
                       % (_e(n), _e(d), _e(dur)) for n, d, dur in items)
        tables.append('''<h2>%s</h2>
    <div class="table-scroll"><table class="table">
      <thead><tr><th>Name</th><th>Description</th><th>Duration</th></tr></thead>
      <tbody>%s</tbody>
    </table></div>''' % (_e(group), body))

    out = [c_page_head(
        H, depth, 'Legal', 'Cookie Policy', '', 'images/heroes/cookie.jpg',
        c_crumbs(H, depth, [], 'Cookie Policy'), short=True)]
    out.append('''<section class="legal"><div class="wrap">
  <p class="legal__updated">Last updated 15 May 2026</p>
  <div class="prose">
    <p>This page provides comprehensive information about how we use cookies on our website to enhance your browsing experience, improve website performance, and deliver personalised content. Cookies are small text files that are stored on your device when you visit our site. They help us understand how visitors interact with our website, allowing us to offer a smoother and more efficient user experience.</p>
    <p>In the tables below, you will find detailed information about each type of cookie we use, its purpose, and how long it remains on your device. We are committed to respecting your privacy and providing transparency about the data we collect through cookies. For more information on how we handle your personal data, please see our <a href="privacy-policy.html">Privacy Policy</a>.</p>
    <h2>Managing cookies</h2>
    <p>You can control or delete cookies at any time through your browser settings. Blocking essential cookies may mean parts of this website do not work as intended.</p>
    {tables}
  </div>
</div></section>'''.format(tables='\n    '.join(tables)))
    return '\n'.join(out)


# ---- 404 ---------------------------------------------------------------------
def r_404(depth, H):
    return '''<section class="notfound">
  <div class="wrap">
    <div class="notfound__code">404</div>
    <span class="label">Page not found</span>
    <h1 class="u-mt-4 u-mb-6">We could not find that page.</h1>
    <p class="lead u-measure-c u-mb-8">It may have moved, or the address may be slightly different. Try the treatments overview, or get in touch and we will point you in the right direction.</p>
    <div class="btn-row">{b1}{b2}</div>
  </div>
</section>'''.format(b1=c_btn('Back to home', H.rel('home', depth), 'solid'),
                     b2=c_btn('Contact us', H.rel('contact', depth), 'outline'))


# ---- Style guide -------------------------------------------------------------
SWATCHES = [
    ('Ink', '--black', '#0E1116'), ('Ink 800', '--black-800', '#1A1F26'),
    ('Paper', '--paper', '#F7F6F3'), ('Paper 3', '--paper-3', '#EFEDE8'),
    ('Ink soft', '--ink-soft', '#5B615F'), ('Ink mute', '--ink-mute', '#8A8F8C'),
    ('Line', '--line', '#D9D7D0'), ('Accent', '--accent', '#17A6DE'),
    ('Accent 600', '--accent-600', '#1189BB'), ('Success', '--ok', '#1D7A57'),
    ('Warning', '--warn', '#8A5A00'), ('Error', '--error', '#A93226'),
]

TYPE_ROWS = [
    ('Display', 'display', '--fs-hero', '30 → 68px', 'A calmer kind of dental care.'),
    ('Heading 1', 'h1', '--fs-h1', '28 → 52px', 'Every treatment starts with a conversation.'),
    ('Heading 2', 'h2', '--fs-h2', '24 → 34px', 'Four areas of care.'),
    ('Heading 3', 'h3', '--fs-h3', '20 → 24px', 'What to expect at your first visit'),
    ('Heading 4', 'h4', '--fs-h4', '17px', 'Preventative care'),
    ('Lead', 'lead', '--fs-lead', '15 → 17px',
     'Routine dental appointments are essential to maintain good oral health.'),
    ('Body', 'body', '--fs-body', '15px',
     'We take time to understand your concerns, respect your choices, and explain your options clearly.'),
    ('Label', 'label', '--fs-label', '11px / .16em', 'Preventative dentistry'),
]

SPACE_STEPS = [('s-1', 4), ('s-2', 8), ('s-3', 12), ('s-4', 16), ('s-5', 20), ('s-6', 24),
               ('s-7', 32), ('s-8', 44), ('s-9', 56), ('s-10', 72), ('s-11', 88), ('s-12', 112)]


def _sg(title, eyebrow, demo):
    return ('<section class="sg-section"><span class="label">%s</span><h2>%s</h2>%s</section>'
            % (_e(eyebrow), _e(title), demo))


def r_styleguide(depth, H):
    out = [c_page_head(
        H, depth, 'Design system', 'Style guide',
        'A living reference for every token and component used across the site.',
        None, c_crumbs(H, depth, [], 'Style guide'), short=True)]

    body = []

    # Colour
    chips = ''.join(
        '<div class="sg-swatch"><div class="sg-swatch__chip" style="background:var(%s)"></div>'
        '<div class="sg-swatch__name">%s</div><div class="sg-swatch__val">var(%s) &middot; %s</div></div>'
        % (var, _e(name), var, val) for name, var, val in SWATCHES)
    body.append(_sg('Colour', '01', '<div class="sg-swatches">%s</div>' % chips))

    # Type
    rows = []
    for name, cls, var, size, sample in TYPE_ROWS:
        if cls in ('h1', 'h2', 'h3', 'h4'):
            markup = '<div class="sg-sample sg-sample--%s">%s</div>' % (cls, _e(sample))
        elif cls == 'display':
            markup = '<div class="sg-sample sg-sample--display">%s</div>' % _e(sample)
        elif cls == 'label':
            markup = '<span class="label">%s</span>' % _e(sample)
        elif cls == 'lead':
            markup = '<p class="lead">%s</p>' % _e(sample)
        else:
            markup = '<p>%s</p>' % _e(sample)
        rows.append('<div class="sg-type-row"><div class="sg-type-row__meta">%s<br>var(%s) &middot; %s</div>'
                    '<div style="flex:1;min-width:min(100%%,320px)">%s</div></div>'
                    % (_e(name), var, _e(size), markup))
    body.append(_sg('Typography', '02',
                    '<p class="lead u-mb-8">Space Grotesk for headings and micro-labels, Inter for '
                    'body copy. The scale is fluid — every size interpolates between a mobile and '
                    'a desktop value.</p>' + ''.join(rows)))

    # Spacing
    boxes = ''.join('<div><div class="sg-scale__box" style="width:%dpx;height:%dpx"></div>'
                    '<div class="sg-scale__label">%s &middot; %dpx</div></div>' % (v, v, n, v)
                    for n, v in SPACE_STEPS)
    body.append(_sg('Spacing', '03',
                    '<p class="lead u-mb-8">A 4px base scale. Sections use the fluid '
                    '<code>--section-y</code> token rather than a fixed step.</p>'
                    '<div class="sg-scale">%s</div>' % boxes))

    # Buttons and links
    body.append(_sg('Buttons & links', '04', '''
      <div class="sg-demo">
        <div class="btn-row u-mb-6">{b1}{b2}{b3}</div>
        <div class="btn-row u-mb-6">{b4}{b5}</div>
        <div class="cluster">{a1}<a class="link-inline" href="#0">An inline text link</a></div>
      </div>
      <div class="sg-demo sg-demo--dark">
        <div class="btn-row u-mb-6">{b6}</div>
        <div class="cluster">{a2}</div>
      </div>'''.format(
        b1=c_btn('Solid button', '#0', 'solid'), b2=c_btn('Outline button', '#0', 'outline'),
        b3='<a class="btn btn--solid is-disabled" href="#0"><span class="btn__fill"></span>'
           '<span class="btn__label">Disabled</span></a>',
        b4='<a class="btn btn--solid btn--sm" href="#0"><span class="btn__fill"></span>'
           '<span class="btn__label">Small solid</span></a>',
        b5='<a class="btn btn--outline btn--sm" href="#0"><span class="btn__fill"></span>'
           '<span class="btn__label">Small outline</span></a>',
        b6=c_btn('Light button', '#0', 'light'),
        a1=c_arc_link('Arc link', '#0'), a2=c_arc_link('Arc link on dark', '#0', light=True))))

    # Badges, notices
    body.append(_sg('Badges & notices', '05', '''
      <div class="sg-demo">
        <div class="cluster u-mb-8">
          <span class="badge">Default</span>
          <span class="badge badge--accent">Accent</span>
          <span class="badge badge--solid">Solid</span>
          <span class="badge pill">Pill</span>
        </div>
        <div class="stack--lg stack">
          <div class="notice"><strong>Information</strong>Members of Our Plan pay a £0 emergency access fee.</div>
          <div class="notice notice--ok"><strong>Success</strong>Your referral has been received.</div>
          <div class="notice notice--warn"><strong>Please note</strong>Fees shown are a guide only.</div>
          <div class="notice notice--error"><strong>Problem</strong>We could not submit that form.</div>
        </div>
      </div>'''))

    # Placeholders
    body.append(_sg('Image placeholder', '05b', '''
      <p class="lead u-mb-8">Every media area on the site is a placeholder until the practice's photography arrives. Replace the whole <code>&lt;div class="ph"&gt;</code> with an <code>&lt;img&gt;</code> — the parent already owns the aspect ratio.</p>
      <div class="cols-3">
        <div><div class="ar-3-2">{a}</div><p class="meta u-mt-2">3:2 — cards, case images</p></div>
        <div><div class="ar-4-3">{b}</div><p class="meta u-mt-2">4:3 — strip tiles</p></div>
        <div><div class="ar-3-4">{c}</div><p class="meta u-mt-2">3:4 — team portraits</p></div>
      </div>'''.format(a=c_ph('A dentist treating a patient'), b=c_ph('Inside the practice'),
                       c=c_ph('Portrait — Dr Martin Sulo'))))

    # Cards & strip
    body.append(_sg('Cards & strip tiles', '06',
                    c_cards(H, depth, [
                      {'key': 'general', 'label': 'Treatments', 'title': 'General dentistry',
                       'text': 'Your trusted local family dental practice for all kinds of general dentistry.',
                       'image': 'images/cards/general-dentistry.jpg', 'alt': ''},
                      {'key': 'cosmetic', 'label': 'Treatments', 'title': 'Cosmetic dentistry',
                       'text': 'Treatments that enhance, align, and whiten or tone your teeth.',
                       'image': 'images/cards/cosmetic-dentistry.jpg', 'alt': ''},
                      {'key': 'preventative', 'label': 'Treatments', 'title': 'Preventative dentistry',
                       'text': 'Routine appointments are essential to maintain good oral health.',
                       'image': 'images/cards/preventative-dentistry.jpg', 'alt': ''}], cols=3)))

    # Facts
    body.append(_sg('Facts', '07', '''
      <div class="sg-demo">
        <div class="facts facts--paper">
          <div class="fact"><div class="fact__num">10%</div><div class="fact__cap">Discount on any treatment</div></div>
          <div class="fact"><div class="fact__num">£0</div><div class="fact__cap">Emergency access fee</div></div>
          <div class="fact"><div class="fact__num">Same day</div><div class="fact__cap">Emergency appointment</div></div>
        </div>
      </div>'''))

    # Process
    body.append(_sg('Process rows', '08', '''
      <div class="p-row"><div class="p-row__num">01</div><div><h3>Consultation</h3><p>A conversation about what is bothering you, or what you would like to improve.</p></div></div>
      <div class="p-row"><div class="p-row__num">02</div><div><h3>Assessment</h3><p>A full examination of teeth, gums, bite and soft tissues.</p></div></div>
      <div class="p-row"><div class="p-row__num">03</div><div><h3>Options and costs</h3><p>Every reasonable option written down, with a fully costed plan.</p></div></div>'''))

    # Specs and price list
    body.append(_sg('Spec rows & price list', '09',
                    '<div class="cols-2"><div>' + c_specs([
                        ('Phone', '<a href="tel:%s">%s</a>' % (SITE['phone_href'], SITE['phone'])),
                        ('Email', '<a href="mailto:%s">%s</a>' % (SITE['email'], SITE['email'])),
                        ('Parking', 'On site, step-free')]) + '</div><div>'
                    '<div class="price-list">'
                    '<div class="price-list__row"><div><strong>2 exams &amp; oral health visits</strong>'
                    '<div class="price-list__note">With small X-rays</div></div><div>£19.95 / month</div></div>'
                    '<div class="price-list__row"><div><strong>3 exams &amp; oral health visits</strong>'
                    '<div class="price-list__note">With small X-rays</div></div><div>£26.25 / month</div></div>'
                    '</div></div></div>'))

    # Accordion
    body.append(_sg('Accordion', '10', c_accordion([
        ('Does root canal treatment hurt?', '<p>The treatment itself is carried out under local '
         'anaesthetic and should feel much like having a filling.</p>'),
        ('How long do implants last?', '<p>With good hygiene and regular maintenance many last '
         'decades.</p>'),
        ('Can I join the membership plan today?', '<p>You will need an initial assessment first '
         'so that we can be sure your mouth is dentally fit.</p>'),
    ], idbase='sg')))

    # Table
    body.append(_sg('Data table', '11',
                    '<div class="table-scroll"><table class="table">'
                    '<thead><tr><th>Name</th><th>Description</th><th>Duration</th></tr></thead>'
                    '<tbody>'
                    '<tr><td><code>_ga</code></td><td>Registers a unique ID used to generate statistical data.</td><td>1 year 1 month</td></tr>'
                    '<tr><td><code>PHPSESSID</code></td><td>Preserves session state across page requests.</td><td>Session</td></tr>'
                    '</tbody></table></div>'))

    # Forms
    body.append(_sg('Form controls', '12', '<div class="sg-demo">' + f_form(
        'sgForm',
        [f_field('sg-name', 'Your name', required=True),
         f_field('sg-email', 'Your email', 'email', required=True),
         f_field('sg-phone', 'Phone', 'tel', hint='Include the area code'),
         f_field('sg-select', 'What is it about?', 'select',
                 options=['Registering as a new patient', 'Booking an appointment', 'Something else']),
         f_field('sg-message', 'Your message', 'textarea', full=True, rows=4),
         f_checks('sg-checks', 'Areas of interest',
                  ['General dentistry', 'Cosmetic dentistry', 'Implants']),
         '<div class="field field--full"><label class="choice">'
         '<input type="checkbox" id="sg-consent" required><span>I agree to be contacted.</span>'
         '</label><span class="field__error" role="alert"></span></div>'],
        'Send message', note='Submit with fields empty to see the validation states.')
        + '</div>'))

    # Multi-step form + repeat group
    def _sg_person(i):
        return [
            f_field('sg-person-%s-name' % i, 'Name', required=True,
                    name='sg-person[%s][name]' % i),
            f_field('sg-person-%s-role' % i, 'Role', 'select', required=True,
                    name='sg-person[%s][role]' % i,
                    options=['Referrer', 'Operating (reporting)', 'Both']),
        ]

    body.append(_sg('Multi-step form & repeat group', '12b', '<div class="sg-demo">' + f_form(
        'sgSteps',
        [f_step('Your details', [
            f_field('sg-s-name', 'Name', required=True),
            f_field('sg-s-email', 'Email', 'email', required=True),
         ]),
         f_step('Your team', [
            f_repeat('sg-person', 'Person', _sg_person, min_items=1, max_items=4,
                     add_label='Add another person'),
         ], intro='A repeat group. Add and remove people — the fields are renamed '
                  'sg-person[0][…], sg-person[1][…] and so on as you go.'),
         f_step('Confirm', [
            f_field('sg-s-notes', 'Anything else?', 'textarea', rows=3),
         ])],
        'Submit', steps=True,
        note='Turn JavaScript off and this becomes one long form with every step '
             'visible and a working submit button.')
        + '</div>'))

    # Chooser
    body.append(_sg('Chooser (tab switcher)', '12c', f_chooser('sg', [
        ('sg-one', 'I am a patient', 'What a patient would fill in', 'Patient panel',
         '<p class="muted">One panel per audience. Turn JavaScript off and the tab row '
         'disappears, leaving both panels visible with their own headings.</p>'),
        ('sg-two', 'I am a professional', 'What a colleague would fill in', 'Professional panel',
         '<p class="muted">Arrow keys move between tabs; the selected tab is written to the '
         'URL hash so links can open a particular panel.</p>'),
    ])))

    # Gallery
    body.append(_sg('Gallery & lightbox', '13', c_gallery(H, depth, [
        ('images/cases/case-worn-1.jpg', 'Before', 'Before treatment'),
        ('images/cases/case-worn-2.jpg', 'After', 'After treatment'),
        ('images/cases/case-worn-3.jpg', 'Detail', 'Detail of the finished work')])))

    # Rail & pager
    body.append(_sg('Rail & pager', '14',
                    '<div class="cols-2 u-mb-8"><div>' + c_rail(H, depth, 'crowns', 'cosmetic')
                    + '</div><div></div></div>' + c_pager(H, depth, 'case-worn', 'case-newdenture')))

    # Quote
    body.append(_sg('Quote carousel', '15', c_quote(TESTIMONIALS[:3])))

    out.append('<div class="wrap section">%s</div>' % ''.join(body))
    out.append(c_cta(H, depth, 'Back to the site.', primary=('Home', 'home'),
                     secondary=('Contact us', 'contact')))
    return '\n'.join(out)
