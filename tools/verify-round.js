const { chromium } = require('playwright');
let fail = 0;
const ok = (n, c, x = '') => { console.log(`${c ? '  PASS' : '  FAIL'}  ${n}${c ? '' : '  << ' + x}`); if (!c) fail++; };
const NARROW = 900;
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.route('**://*.google*/**', r => r.abort());
  const v = Date.now();
  const go = u => p.goto(`http://localhost:8931/${u}?v=${v}`, { waitUntil: 'networkidle' });
  const box = async sel => p.evaluate(s => { const e = document.querySelector(s); if (!e) return null;
    const r = e.getBoundingClientRect(); return { l: Math.round(r.left), r: Math.round(r.right), w: Math.round(r.width) }; }, sel);

  console.log('\n== 1. process: one centred container, head and rows aligned ==');
  await go('pages/implant-clinic.html');
  const pw = await box('.process .wrap'), ph = await box('.process__head'), pr = await box('.p-row');
  ok('container capped near 900', pw.w <= NARROW + 2, `${pw.w}`);
  ok('container is centred', Math.abs(pw.l - (1600 - pw.r)) <= 2, `l=${pw.l} r-gap=${1600 - pw.r}`);
  ok('head and rows share a left edge', ph.l === pr.l, `head=${ph.l} row=${pr.l}`);

  console.log('\n== 2. team: smaller container ==');
  await go('pages/about-us.html');
  const tg = await box('.team__grid'), port = await box('.team__portrait');
  ok('team grid capped near 900', tg.w <= NARROW + 2, `${tg.w}`);
  ok('team grid centred', Math.abs(tg.l - (1600 - tg.r)) <= 2, `l=${tg.l}`);
  ok('portrait no longer enormous', port.w < 480, `portrait=${port.w}`);

  console.log('\n== 3. form: no top rule, intro lines up ==');
  await go('pages/implant-referrals.html');
  const st = await p.evaluate(() => {
    const list = document.querySelector('.stepper__list');
    const btn = document.querySelector('.stepper__btn');
    return { listTop: getComputedStyle(list).borderTopWidth, btnTop: getComputedStyle(btn).borderTopWidth,
             bar: !!document.querySelector('.stepper__bar') };
  });
  ok('no rule above the stepper labels', st.listTop === '0px', st.listTop);
  ok('no per-button top edge either', st.btnTop === '0px', st.btnTop);
  ok('progress bar kept', st.bar);

  await go('pages/referrals.html');
  const intro = await p.evaluate(() => {
    const i = [...document.querySelectorAll('p')].find(x => /CBCT scan or an OPG/.test(x.textContent));
    const f = document.querySelector('.form');
    if (!i || !f) return null;
    return { intro: Math.round(i.getBoundingClientRect().left), form: Math.round(f.getBoundingClientRect().left) };
  });
  ok('intro shares the form column', intro && intro.intro === intro.form, JSON.stringify(intro));

  console.log('\n== 4. fees: one centred container, no ragged column ==');
  await go('pages/fees-and-membership.html');
  const fees = await p.evaluate(() => {
    const h = [...document.querySelectorAll('h3')].find(x => /Your benefits include/.test(x.textContent));
    const ul = document.querySelector('.plan__list');
    const wrap = h.closest('.wrap');
    return { h: Math.round(h.getBoundingClientRect().left), ul: Math.round(ul.getBoundingClientRect().left),
             wrapW: Math.round(wrap.getBoundingClientRect().width), narrow: wrap.classList.contains('wrap--narrow') };
  });
  ok('benefits band is the narrow container', fees.narrow && fees.wrapW <= NARROW + 2, JSON.stringify(fees));
  ok('heading and list share a left edge', fees.h === fees.ul, `h=${fees.h} ul=${fees.ul}`);

  console.log('\n== 5. FAQ narrow ==');
  await go('pages/implant-clinic.html');
  const faq = await p.evaluate(() => {
    const a = document.querySelector('.accordion'); const w = a.closest('.wrap');
    const head = w.querySelector('.section-head');
    return { w: Math.round(w.getBoundingClientRect().width),
             headL: Math.round(head.getBoundingClientRect().left),
             accL: Math.round(a.getBoundingClientRect().left) };
  });
  ok('FAQ container capped near 900', faq.w <= NARROW + 2, `${faq.w}`);
  ok('FAQ head and items aligned', faq.headL === faq.accL, JSON.stringify(faq));

  // 6. The rail is gone entirely — replaced by the prev/next pager.
  //    Covered by verify-pager.js.

  console.log('\n== 7. two equal balanced columns ==');
  await go('pages/referrals.html');
  const cols = await p.evaluate(() => {
    const bdy = document.querySelector('.ed__body--cols');
    const s = getComputedStyle(bdy);
    const ps = [...bdy.querySelectorAll('p')];
    // a paragraph split across the gutter returns a UNION rect spanning both
    // columns, so measure the individual line fragments instead
    const frags = ps.flatMap(x => [...x.getClientRects()]);
    const cols = new Map();
    for (const f of frags) {
      const k = Math.round(f.left);
      if (!cols.has(k)) cols.set(k, { w: Math.round(f.width), top: f.top, bottom: f.bottom });
      const c = cols.get(k);
      c.top = Math.min(c.top, f.top); c.bottom = Math.max(c.bottom, f.bottom);
      c.w = Math.max(c.w, Math.round(f.width));
    }
    const list = [...cols.entries()].sort((a, b) => a[0] - b[0]).map(([l, c]) =>
      ({ left: l, w: c.w, h: Math.round(c.bottom - c.top) }));
    return { count: s.columnCount, gap: s.columnGap, distinctLefts: cols.size, cols: list };
  });
  ok('body is two balanced columns', cols.count === '2', cols.count);
  ok('exactly two column positions', cols.distinctLefts === 2, JSON.stringify(cols));
  ok('the two columns are equal width',
     Math.abs(cols.cols[0].w - cols.cols[1].w) <= 2, JSON.stringify(cols.cols));
  ok('the two columns are balanced in height (within one line)',
     Math.abs(cols.cols[0].h - cols.cols[1].h) <= 30, JSON.stringify(cols.cols));

  console.log('\n== 8. no overflow anywhere touched ==');
  for (const [u, w] of [['pages/fees-and-membership.html', 390], ['pages/about-us.html', 390],
                        ['pages/implant-clinic.html', 390], ['index.html', 1600]]) {
    const q = await b.newPage({ viewport: { width: w, height: 900 } });
    await q.route('**://*.google*/**', r => r.abort());
    await q.goto(`http://localhost:8931/${u}?v=${v}`, { waitUntil: 'domcontentloaded' });
    const o = await q.evaluate(() => ({ s: document.documentElement.scrollWidth, i: window.innerWidth }));
    ok(`${u} @${w} no horizontal overflow`, o.s <= o.i, `${o.s}>${o.i}`);
    await q.close();
  }

  await b.close();
  console.log(fail === 0 ? '\nALL PASSED' : `\n${fail} FAILED`);
  process.exit(fail ? 1 : 0);
})();
