// Every treatment page is reachable from the header, on both desktop and
// mobile. Thirteen leaf pages used to be in neither menu: the Treatments
// dropdown listed only the four categories, so a treatment was findable only
// from its category page or the previous/next pager — that is, if you already
// knew it existed.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = '/home/user/botesdale-dental-clinic';
const all = fs.readdirSync(path.join(ROOT, 'pages')).filter(f => f.endsWith('.html'));

let failed = 0;
const fail = m => { console.log('  FAIL  ' + m); failed++; };

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

  // Which pages ARE treatment pages: a level below Treatments in the trail.
  const ctx0 = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const p0 = await ctx0.newPage();
  await p0.route('**://*.google*/**', r => r.abort());
  const treatments = [];
  for (const f of all) {
    await p0.goto('http://127.0.0.1:8931/pages/' + f, { waitUntil: 'domcontentloaded' });
    const isT = await p0.evaluate(() => {
      const c = document.querySelector('.crumbs');
      if (!c) return false;
      return /Treatments/i.test(c.textContent) &&
             c.querySelectorAll('a, [aria-current]').length >= 3;
    });
    if (isT) treatments.push(f);
  }
  await ctx0.close();
  console.log('\n  ' + treatments.length + ' treatment pages to account for');

  for (const [name, w] of [['desktop header', 1440], ['mobile sheet', 390]]) {
    const before = failed;
    const ctx = await b.newContext({ viewport: { width: w, height: 900 } });
    const p = await ctx.newPage();
    await p.route('**://*.google*/**', r => r.abort());
    await p.goto('http://127.0.0.1:8931/index.html', { waitUntil: 'networkidle' });
    const hrefs = await p.evaluate(sel => [...document.querySelectorAll(sel)]
      .map(a => (a.getAttribute('href') || '').split('/').pop()), w > 1120 ? '.nav__links a' : '.menu a');
    const missing = treatments.filter(f => !hrefs.includes(f));
    if (missing.length) fail(name + ' — not linked: ' + JSON.stringify(missing));
    else if (failed === before)
      console.log('  PASS  ' + name + ': all ' + treatments.length + ' reachable');
    await ctx.close();
  }

  if (treatments.length < 15) fail('only ' + treatments.length + ' treatment pages found — the sweep is not reaching them');

  await b.close();
  console.log(failed ? '\n' + failed + ' FAILED' : '\nALL PASSED');
  process.exit(failed ? 1 : 0);
})();
