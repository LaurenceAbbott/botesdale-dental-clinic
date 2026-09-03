// You must be able to reach the panel with the mouse.
//
// The panel hangs off the HEADER's bottom edge, not the link's, so there is a
// band of dead space between them. On :hover alone the menu closed the instant
// the pointer entered that band — and a diagonal move toward a far column
// crosses it every time. This walks the pointer from the link, through the
// gap, into a link in the LAST column, and clicks it.
const { chromium } = require('playwright');
let failed = 0;
const fail = m => { console.log('  FAIL  ' + m); failed++; };

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const w of [1440, 1280]) {
    console.log('\n== ' + w + 'px ==');
    const before = failed;
    const ctx = await b.newContext({ viewport: { width: w, height: 900 } });
    const p = await ctx.newPage();
    await p.route('**://*.google*/**', r => r.abort());
    await p.goto('http://127.0.0.1:8931/index.html', { waitUntil: 'networkidle' });

    const link = await p.$('.nav__dd--mega > .nav__link');
    const lb = await link.boundingBox();
    await p.mouse.move(lb.x + lb.width / 2, lb.y + lb.height / 2);
    await p.waitForTimeout(250);

    const panel = await p.$('.nav__panel--mega');
    const pb = await panel.boundingBox();
    if (!pb) { fail('panel never opened on hover'); await ctx.close(); continue; }

    // The gap: below the link, above the card.
    const gapY = (lb.y + lb.height + pb.y) / 2;
    if (gapY > lb.y + lb.height) {
      await p.mouse.move(lb.x + lb.width / 2, gapY);
      await p.waitForTimeout(120);
    }

    // Diagonal into the far column, the worst case.
    const last = (await p.$$('.nav__col')).slice(-1)[0];
    const cb = last && await last.boundingBox();
    // No box means the panel shut while the pointer was in the gap — report
    // that, do not throw on a null and leave the run ambiguous.
    if (!cb) { fail('the panel closed while the pointer crossed the gap'); await ctx.close(); continue; }
    await p.mouse.move(cb.x + cb.width / 2, cb.y + 20, { steps: 12 });
    await p.waitForTimeout(200);

    const stillOpen = await p.evaluate(() => {
      const el = document.querySelector('.nav__panel--mega');
      return el && el.getBoundingClientRect().height > 0 && getComputedStyle(el).display !== 'none';
    });
    if (!stillOpen) { fail('the panel closed while the pointer crossed the gap'); await ctx.close(); continue; }

    // And the link under the pointer is actually clickable, not covered.
    const target = await p.$('.nav__col:last-child .nav__col-head');
    const tb = await target.boundingBox();
    const hit = await p.evaluate(([x, y]) => {
      const el = document.elementFromPoint(x, y);
      return !!(el && el.closest('.nav__panel--mega'));
    }, [tb.x + tb.width / 2, tb.y + tb.height / 2]);
    if (!hit) fail('a panel link is not the top element at its own centre');

    await target.click();
    await p.waitForLoadState('domcontentloaded');
    if (!/missing-teeth/.test(p.url())) fail('clicking a panel link did not navigate: ' + p.url());

    if (failed === before) console.log('  PASS  pointer crosses the gap, panel stays open, link navigates');
    await ctx.close();
  }
  await b.close();
  console.log(failed ? '\n' + failed + ' FAILED' : '\nALL PASSED');
  process.exit(failed ? 1 : 0);
})();
