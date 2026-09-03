// Things that DO something should look like it; things that do not, should not.
//
//  - No current-page state anywhere in the menus. The detection was correct
//    (one link, the right page), but it reads as "this one is special"
//    rather than "you are here". data-current survives, unpainted, so the
//    mobile sheet still opens the group you are already in.
//  - The pager title is the whole link, so it takes the link colour.
//  - The accordion +/- is the control you press, so it takes the action
//    colour while the question stays body black.
//  - The burger is drawn from the brand arc, and still recolours when the
//    header goes solid.
const { chromium } = require('playwright');
const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const BASE = 'http://localhost:8931';

let fails = 0;
const bad = (m) => { fails++; console.log('  FAIL ' + m); };
const ok = (m) => console.log('  ok   ' + m);

// --accent-700, the only accent step legible as text on paper (base.css 2.1).
const LINK_BLUE = 'rgb(0, 111, 159)';

(async () => {
  const browser = await chromium.launch({ executablePath: EXE });

  // ---- 1. No painted current-page state, on any page, at either width -----
  for (const vp of [{ width: 1280, height: 900, tag: 'desktop' },
                    { width: 390, height: 844, tag: 'mobile' }]) {
    const ctx = await browser.newContext({ viewport: vp });
    const page = await ctx.newPage();
    await page.route('**://*.google*/**', r => r.abort());
    console.log(`\ncurrent-page state @ ${vp.tag}`);

    // Pages that DO have a current link to mark — a leaf inside a nav group.
    for (const path of ['/pages/veneers.html', '/pages/cosmetic-dentistry.html',
                        '/pages/check-up.html', '/pages/crowns.html']) {
      await page.goto(BASE + path, { waitUntil: 'networkidle' });

      const marked = await page.evaluate(() => document.querySelectorAll('[data-current]').length);
      if (!marked) { bad(`${path}: nothing carries data-current — the sheet cannot open its group`); continue; }

      // The marked link must be painted exactly like its unmarked siblings.
      const diff = await page.evaluate(() => {
        const out = [];
        document.querySelectorAll('.menu__sub a[data-current], .nav__panel a[data-current]').forEach(cur => {
          const sib = [...cur.parentElement.querySelectorAll('a')].find(a => a !== cur);
          if (!sib) return;
          const a = getComputedStyle(cur), b = getComputedStyle(sib);
          ['color', 'backgroundColor', 'fontWeight', 'textDecorationLine'].forEach(p => {
            if (a[p] !== b[p]) out.push(`${cur.className || 'panel link'} ${p}: ${a[p]} vs sibling ${b[p]}`);
          });
        });
        return out;
      });
      if (diff.length) diff.forEach(d => bad(`${path}: current link painted differently — ${d}`));
      else ok(`${path}: current link looks like its siblings (${marked} marked)`);
    }

    // The class that used to do the painting must be gone from sub-links.
    await page.goto(BASE + '/pages/veneers.html', { waitUntil: 'networkidle' });
    const stale = await page.evaluate(() =>
      document.querySelectorAll('.menu__sub a.is-active, .nav__panel a.is-active').length);
    if (stale) bad(`${stale} sub-link(s) still carry .is-active`);
    else ok('no .is-active left on sub-links');

    await ctx.close();
  }

  // ---- 2. Pager titles and accordion controls carry the action colour -----
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  await page.route('**://*.google*/**', r => r.abort());

  console.log('\npager');
  await page.goto(BASE + '/pages/veneers.html', { waitUntil: 'networkidle' });
  const titles = await page.evaluate(() =>
    [...document.querySelectorAll('.pager__title')].map(t => getComputedStyle(t).color));
  if (!titles.length) bad('no .pager__title to check — the fixture has moved');
  else if (titles.some(c => c !== 'rgb(0, 111, 159)'))
    bad(`pager title is ${titles.find(c => c !== 'rgb(0, 111, 159)')}, want the link blue`);
  else ok(`${titles.length} pager title(s) in the link blue`);

  console.log('\naccordion');
  const acc = await page.evaluate(() => {
    const icon = document.querySelector('.accordion__icon');
    if (!icon) return null;
    const btn = icon.closest('.accordion__btn');
    return {
      bar: getComputedStyle(icon, '::before').backgroundColor,
      label: getComputedStyle(btn).color,
    };
  });
  if (!acc) bad('no .accordion__icon to check — the fixture has moved');
  else {
    if (acc.bar !== LINK_BLUE) bad(`accordion +/- is ${acc.bar}, want the link blue`);
    else ok('accordion +/- in the link blue');
    // The question is copy, not a control; only the +/- is the action.
    if (acc.label === LINK_BLUE) bad('the question text went blue too — only the +/- is the action');
    else ok('the question stays body black');
  }

  // ---- 3. The burger is arcs, and still recolours on a solid header -------
  console.log('\nburger');
  const ctxm = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const pm = await ctxm.newPage();
  await pm.route('**://*.google*/**', r => r.abort());
  await pm.goto(BASE + '/index.html', { waitUntil: 'networkidle' });

  const burger = await pm.evaluate(() => {
    const b = document.querySelector('.nav__toggle');
    if (!b) return null;
    const paths = [...b.querySelectorAll('path')];
    return {
      bars: b.querySelectorAll('span').length,
      paths: paths.length,
      curved: paths.every(p => /Q/.test(p.getAttribute('d') || '')),
      stroke: paths.length ? getComputedStyle(paths[0]).stroke : null,
      visible: getComputedStyle(b).display !== 'none',
      colour: getComputedStyle(b).color,
    };
  });
  if (!burger) bad('no .nav__toggle');
  else {
    if (!burger.visible) bad('the burger is not shown at 390px');
    if (burger.bars) bad(`${burger.bars} straight <span> bar(s) left`);
    if (burger.paths !== 3) bad(`${burger.paths} arc(s), want 3`);
    else if (!burger.curved) bad('the burger paths are straight — no Q curve');
    else ok('three arc strokes, drawn with the brand curve');
    if (burger.stroke !== burger.colour) bad(`stroke ${burger.stroke} does not follow color ${burger.colour}`);
    else ok('stroke follows currentColor');
  }

  // Scrolling flips the header to solid; the burger has to follow it or it
  // vanishes into the paper.
  const before = burger && burger.colour;
  await pm.evaluate(() => window.scrollTo(0, 900));
  await pm.waitForTimeout(500);
  const after = await pm.evaluate(() => {
    const b = document.querySelector('.nav__toggle');
    return { colour: getComputedStyle(b).color, stroke: getComputedStyle(b.querySelector('path')).stroke };
  });
  if (after.colour === before) bad(`burger stayed ${after.colour} when the header went solid`);
  else ok(`burger recolours on scroll (${before} -> ${after.colour})`);
  if (after.stroke !== after.colour) bad('stroke stopped following currentColor after scroll');

  await browser.close();
  console.log(fails ? `\n${fails} FAILURE(S)` : '\nALL PASS');
  process.exit(fails ? 1 : 0);
})();
