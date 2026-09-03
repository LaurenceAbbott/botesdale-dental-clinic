const { chromium } = require('playwright');
let fail = 0;
const ok = (n, c, x = '') => { console.log(`${c ? '  PASS' : '  FAIL'}  ${n}${c ? '' : '  << ' + x}`); if (!c) fail++; };
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const v = Date.now();
  for (const w of [1600, 2200, 1280, 900]) {
    const p = await b.newPage({ viewport: { width: w, height: 1000 } });
    await p.route('**://*.google*/**', r => r.abort());
    await p.goto(`http://localhost:8931/index.html?v=${v}`, { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(400);
    const r = await p.evaluate(() => {
      const eds = [...document.querySelectorAll('.ed')];
      // Reference is the container's TEXT line: the .wrap content box, i.e.
      // where the copy column starts — not the viewport edge.
      const wrapEl = document.querySelector('.section .wrap');
      const ws = getComputedStyle(wrapEl);
      const wr = wrapEl.getBoundingClientRect();
      const wb = { left: wr.left + parseFloat(ws.paddingLeft), right: wr.right - parseFloat(ws.paddingRight) };
      const out = eds.map(e => {
        const m = e.querySelector('.ed__media').getBoundingClientRect();
        const eb = e.getBoundingClientRect();
        const rev = e.classList.contains('ed--rev');
        // how far the picture reaches past the container's text line
        const overhang = rev ? Math.round(m.right - wb.right) : Math.round(wb.left - m.left);
        const fromViewport = rev ? Math.round(eb.right - m.right) : Math.round(m.left - eb.left);
        return { rev, overhang, fromViewport, pt: Math.round(parseFloat(getComputedStyle(e).paddingTop)) };
      });
      return { out, margin: Math.round(wb.left), scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth };
    });
    console.log(`\n== ${w}px ==  outer margin to text line = ${r.margin}`);
    ok('no horizontal overflow', r.scrollW <= r.innerW, `${r.scrollW}>${r.innerW}`);
    ok('every ed has top padding', r.out.every(o => o.pt > 20), JSON.stringify(r.out.map(o => o.pt)));
    ok('media never reaches the viewport edge', r.out.every(o => o.fromViewport > 0), JSON.stringify(r.out.map(o => o.fromViewport)));
    ok('overhang is ~10% of the outer margin', r.out.every(o => Math.abs(o.overhang - r.margin * 0.1) <= 2),
       `overhang=${r.out[0].overhang} expected≈${(r.margin*0.1).toFixed(1)}`);
    await p.close();
  }
  // two-column body
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.route('**://*.google*/**', r => r.abort());
  await p.goto(`http://localhost:8931/pages/referrals.html?v=${v}`, { waitUntil: 'domcontentloaded' });
  await p.locator('.ed__body--cols').first().scrollIntoViewIfNeeded();
  await p.waitForTimeout(1200);  // let the reveal transition settle before measuring
  const c = await p.evaluate(() => {
    const body = document.querySelector('.ed__body--cols');
    if (!body) return null;
    // Balanced multi-column, not a grid: a paragraph may be split across the
    // gutter, so measure line fragments and group them into columns.
    const ps = [...body.querySelectorAll('p')];
    const frags = ps.flatMap(x => [...x.getClientRects()]);
    const cols = new Map();
    for (const f of frags) {
      const k = Math.round(f.left);
      if (!cols.has(k)) cols.set(k, { w: 0, top: f.top, bottom: f.bottom });
      const c = cols.get(k);
      c.w = Math.max(c.w, Math.round(f.width));
      c.top = Math.min(c.top, f.top); c.bottom = Math.max(c.bottom, f.bottom);
    }
    const list = [...cols.entries()].sort((a, b) => a[0] - b[0]).map(([l, c]) => ({ l, w: c.w, h: Math.round(c.bottom - c.top) }));
    return { n: ps.length, cols: list,
             sideBySide: list.length === 2 && Math.abs(list[0].w - list[1].w) <= 2
                         && Math.abs(list[0].h - list[1].h) <= 30,
             h2Wide: getComputedStyle(document.querySelector('.ed--cols .ed__text h2')).maxWidth };
  });
  console.log('\n== two-column body ==');
  ok('long copy runs two columns', c && c.sideBySide, JSON.stringify(c));
  ok('heading is not capped in the two-column variant', c && c.h2Wide === 'none', c && c.h2Wide);

  // nav CTA legibility when scrolled
  await p.goto(`http://localhost:8931/index.html?v=${v}`, { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(300);
  await p.evaluate(() => window.scrollTo(0, 1200));
  await p.waitForTimeout(700);
  const n = await p.evaluate(() => {
    const cta = document.querySelector('.nav__cta');
    const nav = document.querySelector('.nav');
    // compare against the token, not a hardcoded hex, so a palette change
    // does not read as a regression here
    const probe = document.createElement('span');
    probe.style.color = 'var(--black)';
    document.body.appendChild(probe);
    const ink = getComputedStyle(probe).color;
    probe.remove();
    return { scrolled: nav.classList.contains('is-scrolled'), color: getComputedStyle(cta).color, ink };
  });
  ok('header goes solid on scroll', n.scrolled);
  ok('scrolled CTA label is ink, not paper', n.color === n.ink, `${n.color} vs ink ${n.ink}`);
  await b.close();
  console.log(fail === 0 ? '\nALL PASSED' : `\n${fail} FAILED`);
})();
