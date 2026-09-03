// A treatment page gets ONE picture, and it is the header hero.
//
// This was reported twice: first the .ed under the head on the category pages,
// then the figure in the prose on the leaf pages. Both showed the same subject
// the hero had already shown, a screen further down, captioned with the page
// title the h1 had already said.
//
// Navigational thumbnails are not a second picture — a category page's strip of
// child treatments is a menu, not a photograph of the subject — so those are
// the one thing allowed through.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = '/home/user/botesdale-dental-clinic';
const pages = fs.readdirSync(path.join(ROOT, 'pages')).filter(f => f.endsWith('.html')).map(f => 'pages/' + f);

let failed = 0;
const fail = m => { console.log('  FAIL  ' + m); failed++; };

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await ctx.newPage();
  await p.route('**://*.google*/**', r => r.abort());

  let treatment = 0, clean = 0;
  for (const u of pages) {
    const resp = await p.goto('http://127.0.0.1:8931/' + u, { waitUntil: 'domcontentloaded' });
    if (!resp || resp.status() !== 200) { fail(u + ' returned ' + (resp && resp.status())); continue; }
    const r = await p.evaluate(() => {
      const crumbs = document.querySelector('.crumbs');
      if (!crumbs) return null;
      const trail = crumbs.textContent.replace(/\s+/g, ' ');
      if (!/Treatments/i.test(trail)) return null;          // not a treatment page
      // Home / Treatments is the HUB — its rows are the four areas of care,
      // which is the page's content, not a picture of a subject it has
      // already shown. A page ABOUT a treatment sits a level deeper.
      const depth = crumbs.querySelectorAll('a, [aria-current]').length;
      if (depth < 3) return null;
      const extras = [...document.querySelectorAll('.ph, img')]
        .filter(e => !e.closest('.nav, .footer, .lightbox, .page-head, .hero'))
        // a menu of child treatments, not a photograph of the subject
        .filter(e => !e.closest('.strip__media, .card__media'))
        .map(e => e.getAttribute('aria-label') || e.alt || e.tagName.toLowerCase());
      return { extras, head: !!document.querySelector('.page-head') };
    });
    if (!r) continue;
    treatment++;
    if (!r.head) fail(u + ' — treatment page with no header hero at all');
    else if (r.extras.length) fail(u + ' — a second picture below the hero: ' + JSON.stringify(r.extras));
    else clean++;
  }

  if (treatment < 15) fail('only ' + treatment + ' treatment pages seen — the sweep is not reaching them');
  else if (!failed) console.log('  PASS  ' + clean + ' treatment pages carry one picture, in the hero');

  await b.close();
  console.log(failed ? '\n' + failed + ' FAILED' : '\nALL PASSED');
  process.exit(failed ? 1 : 0);
})();
