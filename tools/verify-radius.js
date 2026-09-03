// Photography is rounded at 32px; structure stays square (design.md principle 2).
//
// The radius goes on the OUTERMOST object. For a lone image that is the image
// itself or the box that clips it; for a hairline-joined row (.strip__row) it
// is the whole row, not each tile; for a standalone card it is the card. So
// this does not look for a radius on the image — it walks up until something
// actually clips with a curve, and fails if nothing does.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = '/home/user/botesdale-dental-clinic';
const pages = ['index.html', '404.html'].concat(
  fs.readdirSync(path.join(ROOT, 'pages')).filter(f => f.endsWith('.html')).map(f => 'pages/' + f));

const WANT = 32;
let failed = 0;
const fail = m => { console.log('  FAIL  ' + m); failed++; };

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const w of [390, 1440]) {
    console.log('\n== ' + w + 'px ==');
    const before = failed;
    const ctx = await b.newContext({ viewport: { width: w, height: 900 } });
    const p = await ctx.newPage();
    await p.route('**://*.google*/**', r => r.abort());
    let checked = 0, square = 0;
    for (const u of pages) {
      const resp = await p.goto('http://127.0.0.1:8931/' + u, { waitUntil: 'domcontentloaded' });
      if (!resp || resp.status() !== 200) { fail(u + ' returned ' + (resp && resp.status())); continue; }
      const r = await p.evaluate((want) => {
        const cls = e => e.className && typeof e.className === 'string'
          ? '.' + e.className.trim().split(/\s+/)[0] : e.tagName.toLowerCase();
        const bad = [], ok = [];
        for (const el of document.querySelectorAll('img, .ph')) {
          // The brand mark is a logo, not photography. The hero and page-head
          // panels are clipped to the arc (#heroArc) — that IS their corner
          // treatment, and a radius would fight it.
          if (el.closest('.nav, .footer, .brand')) continue;
          if (el.matches('.hero__media, .page-head__media')) continue;
          let n = el, found = null;
          while (n && n !== document.body) {
            if (parseFloat(getComputedStyle(n).borderRadius) >= want - 0.5) { found = cls(n); break; }
            n = n.parentElement;
          }
          (found ? ok : bad).push(cls(el) + (found ? ' via ' + found : ''));
        }
        return { bad, n: ok.length + bad.length };
      }, WANT);
      checked += r.n; square += r.bad.length;
      for (const x of [...new Set(r.bad)])
        fail(u + ' — ' + x + ' has no rounded object above it');
    }
    if (checked < 100) fail('only ' + checked + ' images seen at ' + w + 'px — the sweep is not reaching them');
    else if (failed === before)
      console.log('  PASS  ' + checked + ' images, every one inside a ' + WANT + 'px corner (' + square + ' square)');
    await ctx.close();
  }
  await b.close();
  console.log(failed ? '\n' + failed + ' FAILED' : '\nALL PASSED');
  process.exit(failed ? 1 : 0);
})();
