// The style guide has to describe the system that exists.
//
// It listed a "Lead" row for --fs-lead at "15 → 17px" long after that token
// was deleted, and omitted --fs-sm and --fs-xs entirely — so the one page
// whose job is to document the scale was documenting a scale we no longer
// ship. Two checks:
//
//   1. Every --fs-* token in base.css has a row, and every row names a token
//      that exists. That is what catches a deleted or a new one.
//   2. Each specimen RENDERS at the size its row claims — a fixed size exactly,
//      a fluid range within its bounds.
const { chromium } = require('playwright');
const fs = require('fs');

const ROOT = '/home/user/botesdale-dental-clinic';
let failed = 0;
const fail = m => { console.log('  FAIL  ' + m); failed++; };

(async () => {
  const base = fs.readFileSync(ROOT + '/css/base.css', 'utf8');
  const block = base.slice(base.indexOf(':root'), base.indexOf('--lh-tight'));
  const tokens = [...new Set([...block.matchAll(/--fs-([a-z0-9]+)\s*:/g)].map(m => 'fs-' + m[1]))];

  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const ctx = await b.newContext({ viewport: { width: 1200, height: 900 } });
  const p = await ctx.newPage();
  await p.route('**://*.google*/**', r => r.abort());
  const resp = await p.goto('http://127.0.0.1:8931/pages/style-guide.html', { waitUntil: 'networkidle' });
  if (!resp || resp.status() !== 200) { fail('style guide returned ' + (resp && resp.status())); }

  const rows = await p.evaluate(() => [...document.querySelectorAll('.sg-type-row')].map(row => {
    const meta = row.querySelector('.sg-type-row__meta').textContent.replace(/\s+/g, ' ');
    const spec = row.querySelector('div:last-child > *');
    return { meta, px: parseFloat(getComputedStyle(spec).fontSize) };
  }));

  console.log('\n== every --fs token has a row, and every row a token ==');
  const named = rows.map(r => (r.meta.match(/var\(--(fs-[a-z0-9]+)\)/) || [])[1]).filter(Boolean);
  const undocumented = tokens.filter(t => !named.includes(t));
  const phantom = named.filter(n => !tokens.includes(n));
  if (undocumented.length) fail('token(s) with no row: ' + JSON.stringify(undocumented));
  if (phantom.length) fail('row(s) naming a token that no longer exists: ' + JSON.stringify(phantom));
  if (!undocumented.length && !phantom.length)
    console.log('  PASS  ' + tokens.length + ' tokens, ' + named.length + ' rows, exactly matched');

  console.log('\n== each specimen renders at the size its row claims ==');
  let ok = 0;
  for (const r of rows) {
    const label = (r.meta.match(/var\(--(fs-[a-z0-9]+)\)/) || ['', '?'])[1];
    const range = r.meta.match(/(\d+)\s*→\s*(\d+)px/);
    const fixed = r.meta.match(/·\s*(\d+)px/);
    if (range) {
      const [lo, hi] = [+range[1], +range[2]];
      if (r.px < lo - 0.5 || r.px > hi + 0.5)
        fail(label + ' claims ' + lo + '→' + hi + 'px but renders ' + r.px);
      else ok++;
    } else if (fixed) {
      if (Math.abs(r.px - +fixed[1]) > 0.5)
        fail(label + ' claims ' + fixed[1] + 'px but renders ' + r.px);
      else ok++;
    } else fail(label + ' row states no size');
  }
  if (ok === rows.length) console.log('  PASS  all ' + ok + ' specimens match their stated size');

  await b.close();
  console.log(failed ? '\n' + failed + ' FAILED' : '\nALL PASSED');
  process.exit(failed ? 1 : 0);
})();
