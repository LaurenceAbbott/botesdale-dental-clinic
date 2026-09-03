const { chromium } = require('playwright');
let fail = 0;
const ok = (n, c, x = '') => { console.log(`${c ? '  PASS' : '  FAIL'}  ${n}${c ? '' : '  << ' + x}`); if (!c) fail++; };
const fs = require('fs');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  await p.route('**://*.google*/**', r => r.abort());
  const v = Date.now();
  const pages = ['index.html', ...fs.readdirSync('/home/user/botesdale-dental-clinic/pages')
    .filter(f => f.endsWith('.html')).map(f => 'pages/' + f)];

  console.log('\n== one primary per page ==');
  const noPrimary = [], multi = [];
  for (const u of pages) {
    if (u.includes('style-guide')) continue;   // a gallery of every variant, by design
    await p.goto(`http://localhost:8931/${u}?v=${v}`, { waitUntil: 'domcontentloaded' });
    const r = await p.evaluate(() => {
      const solids = [...document.querySelectorAll('.btn--solid')]
        .filter(el => el.offsetParent !== null && !el.closest('.cookie'));
      const hasForm = !!document.querySelector('form .btn[type=submit], form button[type=submit]');
      return { n: solids.length, labels: solids.map(s => s.textContent.trim().slice(0, 26)), hasForm };
    });
    if (r.n === 0 && !r.hasForm) noPrimary.push(u);
    if (r.n > 1) multi.push(`${u}: ${JSON.stringify(r.labels)}`);
  }
  ok(`no page is left without a primary action`, noPrimary.length === 0, JSON.stringify(noPrimary));
  ok(`no page has more than one primary`, multi.length === 0, JSON.stringify(multi));

  console.log('\n== dark bands now carry a primary ==');
  await p.goto(`http://localhost:8931/pages/implant-clinic.html?v=${v}`, { waitUntil: 'domcontentloaded' });
  const dark = await p.evaluate(() => {
    const band = document.querySelector('.cta--dark');
    if (!band) return null;
    const solid = band.querySelector('.btn--solid');
    const light = band.querySelector('.btn--light');
    return { hasSolid: !!solid, solidText: solid && solid.textContent.trim(),
             hasSecondary: !!light, secondaryText: light && light.textContent.trim(),
             bg: solid && getComputedStyle(solid).backgroundColor };
  });
  ok('the dark band has a solid primary', dark && dark.hasSolid, JSON.stringify(dark));
  ok('the primary is the implant referral form', dark && /Implant referrals/i.test(dark.solidText || ''), dark && dark.solidText);
  ok('the secondary is still there and not solid', dark && dark.hasSecondary, JSON.stringify(dark));

  console.log('\n== implant section no longer has a pager ==');
  for (const u of ['pages/implant-clinic.html', 'pages/implant-referrals.html', 'pages/missing-teeth.html']) {
    await p.goto(`http://localhost:8931/${u}?v=${v}`, { waitUntil: 'domcontentloaded' });
    const has = await p.evaluate(() => !!document.querySelector('.pager'));
    ok(`${u}: no pager`, !has);
  }
  await p.goto(`http://localhost:8931/pages/crowns.html?v=${v}`, { waitUntil: 'domcontentloaded' });
  ok('treatment pages still have one', await p.evaluate(() => !!document.querySelector('.pager')));

  console.log('\n== pager widths ==');
  for (const w of [390, 768, 1400]) {
    const q = await b.newPage({ viewport: { width: w, height: 900 } });
    await q.route('**://*.google*/**', r => r.abort());
    // two items — veneers, mid-sequence in Cosmetic. Crowns was the example
    // until it moved to Missing teeth and became the first sibling there,
    // where it has a next and no previous.
    await q.goto(`http://localhost:8931/pages/veneers.html?v=${v}`, { waitUntil: 'domcontentloaded' });
    const two = await q.evaluate(() => {
      const pg = document.querySelector('.pager');
      const its = [...pg.querySelectorAll('.pager__item')];
      const pb = pg.getBoundingClientRect();
      const r = its.map(i => i.getBoundingClientRect());
      return { n: its.length, sameRow: Math.abs(r[0].top - r[1].top) < 2,
               halves: r.every(x => Math.abs(x.width - pb.width / 2) <= 2),
               centred: its.every(i => getComputedStyle(i).textAlign === 'center') };
    });
    ok(`${w}px: two items sit 50/50 on one row`, two.n === 2 && two.sameRow && two.halves, JSON.stringify(two));
    ok(`${w}px: text centred`, two.centred);
    // one item
    await q.goto(`http://localhost:8931/pages/gum-reshaping.html?v=${v}`, { waitUntil: 'domcontentloaded' });
    const one = await q.evaluate(() => {
      const pg = document.querySelector('.pager');
      const its = [...pg.querySelectorAll('.pager__item')];
      return { n: its.length,
               full: Math.abs(its[0].getBoundingClientRect().width - pg.getBoundingClientRect().width) <= 1 };
    });
    ok(`${w}px: a lone item spans the full width`, one.n === 1 && one.full, JSON.stringify(one));
    const o = await q.evaluate(() => ({ s: document.documentElement.scrollWidth, i: window.innerWidth }));
    ok(`${w}px: no horizontal overflow`, o.s <= o.i, `${o.s}>${o.i}`);
    await q.close();
  }

  await b.close();
  console.log(fail === 0 ? '\nALL PASSED' : `\n${fail} FAILED`);
  process.exit(fail ? 1 : 0);
})();
