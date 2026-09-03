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

    // Open the menu for real. Being in the DOM is NOT reachable: the sheet's
    // sub-panel is `overflow: hidden` with a max-height, so a link past the cap
    // is present, findable by querySelectorAll, and invisible on the phone.
    // That is exactly how Crowns onwards went missing while this passed.
    if (w <= 1120) {
      await p.click('#menuOpen'); await p.waitForTimeout(400);
      for (const t of await p.$$('.menu__toggle')) {
        for (let i = 0; i < 3; i++) {
          if (await t.getAttribute('aria-expanded') === 'true') break;
          await t.click(); await p.waitForTimeout(300);
        }
      }
      await p.waitForTimeout(400);
    } else {
      await p.hover('.nav__dd--mega .nav__link'); await p.waitForTimeout(300);
    }

    const seen = await p.evaluate(sel => {
      const out = [];
      for (const a of document.querySelectorAll(sel)) {
        const r = a.getBoundingClientRect();
        if (r.width < 1 || r.height < 1) continue;
        // Not clipped away by an ancestor that hides its overflow.
        let n = a.parentElement, clipped = false;
        while (n && n !== document.body) {
          const cs = getComputedStyle(n);
          if (cs.overflow === 'hidden' || cs.overflowY === 'hidden') {
            const b = n.getBoundingClientRect();
            if (r.bottom > b.bottom + 1 || r.top < b.top - 1) { clipped = true; break; }
          }
          n = n.parentElement;
        }
        if (!clipped) out.push((a.getAttribute('href') || '').split('/').pop());
      }
      return out;
    }, w > 1120 ? '.nav__links a' : '.menu a');

    const missing = treatments.filter(f => !seen.includes(f));
    if (missing.length) fail(name + ' — present but not actually visible: ' + JSON.stringify(missing));
    else if (failed === before)
      console.log('  PASS  ' + name + ': all ' + treatments.length + ' visible and unclipped');
    await ctx.close();
  }

  if (treatments.length < 15) fail('only ' + treatments.length + ' treatment pages found — the sweep is not reaching them');

  await b.close();
  console.log(failed ? '\n' + failed + ' FAILED' : '\nALL PASSED');
  process.exit(failed ? 1 : 0);
})();
