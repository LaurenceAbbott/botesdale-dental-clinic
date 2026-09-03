// A hero is a composition; it must not restage itself while you drag a window
// edge. These panels were sized in vh, so on a vertically resizable desktop
// window the copy slid around inside them and the arc travelled up and down the
// photograph. Above phone widths the heights are fixed, and this proves it:
// same width, four very different window heights, identical panel height.
//
// Phones are exempt on purpose — there the viewport IS the device (667 to 932),
// a fixed value that suits one is wrong on the other, and nobody resizes a
// phone window. So below 480 the check flips: the height is EXPECTED to track.
const { chromium } = require('playwright');

const PAGES = [
  ['index.html', '.hero'],
  ['pages/about-us.html', '.page-head'],      // --shot, carries the photograph
  ['pages/treatments.html', '.page-head'],
  ['pages/privacy-policy.html', '.page-head'],// --short
];
const HEIGHTS = [620, 760, 900, 1180];
let failed = 0;
const fail = m => { console.log('  FAIL  ' + m); failed++; };

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

  for (const w of [1440, 1024, 768]) {
    console.log('\n== ' + w + 'px wide — height must not follow the window ==');
    const before = failed;
    for (const [u, sel] of PAGES) {
      const seen = [];
      for (const h of HEIGHTS) {
        const ctx = await b.newContext({ viewport: { width: w, height: h } });
        const p = await ctx.newPage();
        await p.route('**://*.google*/**', r => r.abort());
        await p.goto('http://127.0.0.1:8931/' + u, { waitUntil: 'domcontentloaded' });
        seen.push(await p.evaluate(s => {
          const e = document.querySelector(s);
          return e ? +e.getBoundingClientRect().height.toFixed(1) : null;
        }, sel));
        await ctx.close();
      }
      if (seen.some(v => v === null)) { fail(u + ' — ' + sel + ' not found'); continue; }
      const spread = Math.max(...seen) - Math.min(...seen);
      if (spread > 0.5)
        fail(u + ' ' + sel + ' moves with the window: ' +
             HEIGHTS.map((h, i) => h + 'px->' + seen[i]).join(', '));
    }
    if (failed === before) console.log('  PASS  every panel holds one height across 620-1180px windows');
  }

  // The phone exemption is deliberate, so assert it rather than leaving it
  // untested — if these ever stop tracking, someone has hard-coded a height
  // that will be wrong on half the devices out there.
  console.log('\n== 390px wide — phones are expected to track the viewport ==');
  {
    const before = failed;
    const seen = [];
    for (const h of [667, 932]) {
      const ctx = await b.newContext({ viewport: { width: 390, height: h } });
      const p = await ctx.newPage();
      await p.route('**://*.google*/**', r => r.abort());
      await p.goto('http://127.0.0.1:8931/pages/about-us.html', { waitUntil: 'domcontentloaded' });
      seen.push(await p.evaluate(() => +document.querySelector('.page-head').getBoundingClientRect().height.toFixed(1)));
      await ctx.close();
    }
    if (seen[1] <= seen[0])
      fail('the phone page head did not grow with the viewport (' + seen.join(' -> ') + ')');
    if (failed === before) console.log('  PASS  page head tracks the device: ' + seen.join(' -> '));
  }

  await b.close();
  console.log(failed ? '\n' + failed + ' FAILED' : '\nALL PASSED');
  process.exit(failed ? 1 : 0);
})();
