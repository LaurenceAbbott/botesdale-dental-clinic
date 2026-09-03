// Three things about editorial rows, all of which were wrong on About us:
//
//  1. Every .ed picture is the SAME SIZE within a page. The media used to take
//     its height from whatever the copy column happened to be, so the same
//     component drew a different-sized picture in every block.
//  2. Consecutive rows CHECKERBOARD — media right, left, right — rather than
//     stacking down one side.
//  3. Stacked, COPY COMES FIRST. The picture supports the words; leading with
//     it pushes the heading off a phone screen.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = '/home/user/botesdale-dental-clinic';
const pages = ['index.html', '404.html'].concat(
  fs.readdirSync(path.join(ROOT, 'pages')).filter(f => f.endsWith('.html')).map(f => 'pages/' + f));

let failed = 0;
const fail = m => { console.log('  FAIL  ' + m); failed++; };

const read = p => p.evaluate(() => [...document.querySelectorAll('.ed')].map(ed => {
  const m = ed.querySelector('.ed__media'), t = ed.querySelector('.ed__text');
  if (!m || !t) return null;
  const mb = m.getBoundingClientRect(), tb = t.getBoundingClientRect();
  return { w: +mb.width.toFixed(1), h: +mb.height.toFixed(1),
           side: mb.left > tb.left ? 'right' : 'left',
           copyFirst: tb.top <= mb.top };
}).filter(Boolean));

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

  console.log('\n== 1440px — same size within a page, and alternating ==');
  {
    const before = failed;
    const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } });
    const p = await ctx.newPage();
    await p.route('**://*.google*/**', r => r.abort());
    let rows = 0;
    for (const u of pages) {
      const resp = await p.goto('http://127.0.0.1:8931/' + u, { waitUntil: 'domcontentloaded' });
      if (!resp || resp.status() !== 200) { fail(u + ' returned ' + (resp && resp.status())); continue; }
      const eds = await read(p);
      if (eds.length < 2) { rows += eds.length; continue; }
      rows += eds.length;
      const sizes = [...new Set(eds.map(e => e.w + 'x' + e.h))];
      if (sizes.length > 1) fail(u + ' — .ed pictures are different sizes: ' + sizes.join(', '));
      for (let i = 1; i < eds.length; i++)
        if (eds[i].side === eds[i - 1].side)
          fail(u + ' — rows ' + (i - 1) + ' and ' + i + ' both put the media ' + eds[i].side +
               '; consecutive editorial rows should alternate');
    }
    if (rows < 12) fail('only ' + rows + ' editorial rows seen — the sweep is not reaching them');
    else if (failed === before) console.log('  PASS  ' + rows + ' rows: one picture size per page, sides alternating');
    await ctx.close();
  }

  console.log('\n== 390px — copy above the picture ==');
  {
    const before = failed;
    const ctx = await b.newContext({ viewport: { width: 390, height: 900 } });
    const p = await ctx.newPage();
    await p.route('**://*.google*/**', r => r.abort());
    let rows = 0;
    for (const u of pages) {
      await p.goto('http://127.0.0.1:8931/' + u, { waitUntil: 'domcontentloaded' });
      const eds = await read(p);
      rows += eds.length;
      eds.forEach((e, i) => { if (!e.copyFirst) fail(u + ' — .ed row ' + i + ' puts the image above the copy'); });
    }
    if (rows < 12) fail('only ' + rows + ' rows seen at 390px');
    else if (failed === before) console.log('  PASS  ' + rows + ' rows stack copy-first');
    await ctx.close();
  }

  await b.close();
  console.log(failed ? '\n' + failed + ' FAILED' : '\nALL PASSED');
  process.exit(failed ? 1 : 0);
})();
