const { chromium } = require('playwright');
let fail = 0;
const ok = (n, c, x = '') => { console.log(`${c ? '  PASS' : '  FAIL'}  ${n}${c ? '' : '  << ' + x}`); if (!c) fail++; };
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  await p.route('**://*.google*/**', r => r.abort());
  const v = Date.now();
  const go = u => p.goto(`http://localhost:8931/${u}?v=${v}`, { waitUntil: 'networkidle' });

  console.log('\n== the rail is gone everywhere ==');
  const pages = ['index.html','pages/crowns.html','pages/veneers.html','pages/implant-clinic.html',
                 'pages/case-replacement-of-missing-teeth.html','pages/style-guide.html',
                 'pages/missing-teeth.html','pages/implant-referrals.html'];
  for (const u of pages) {
    await go(u);
    const r = await p.evaluate(() => ({
      rail: document.querySelectorAll('.rail, .with-rail, .rail__list').length,
      loaded: !!document.querySelector('.nav'),
    }));
    ok(`${u}: no rail markup`, r.loaded && r.rail === 0, JSON.stringify(r));
  }

  console.log('\n== pager present, at the foot, after the content ==');
  for (const [u, wantPrev, wantNext] of [
      // Veneers sits mid-sequence in Cosmetic, so it is the two-item case.
      // Crowns used to be, until it moved to Missing teeth and became the
      // first sibling there — one link, not two.
      ['pages/veneers.html', true, true],
      ['pages/crowns.html', false, true],
      // First sibling in its group: next only. It used to page BACK to the
      // category overview, which is a level up rather than a step sideways —
      // "previous: Cosmetic dentistry" from inside Cosmetic dentistry.
      ['pages/clear-aligner.html', false, true],
      ['pages/gum-reshaping.html', true, false],        // last in its group
      ['pages/case-replacement-of-missing-teeth.html', true, true]]) {
    await go(u);
    const r = await p.evaluate(() => {
      const pg = document.querySelector('.pager');
      if (!pg) return null;
      const prev = pg.querySelector('.pager__item--prev'), next = pg.querySelector('.pager__item--next');
      const main = document.querySelector('main');
      const proseSections = [...document.querySelectorAll('.prose, .process, .accordion')];
      const lastContent = proseSections.length ? proseSections[proseSections.length - 1].getBoundingClientRect().bottom : 0;
      const cta = document.querySelector('.cta, .statement');
      return {
        prev: !!prev, next: !!next,
        prevText: prev && prev.querySelector('.pager__title').textContent.trim(),
        nextText: next && next.querySelector('.pager__title').textContent.trim(),
        afterContent: pg.getBoundingClientRect().top >= lastContent - 1,
        beforeCta: !cta || pg.getBoundingClientRect().top < cta.getBoundingClientRect().top,
        nextCol: next ? getComputedStyle(next).gridColumnStart : null,
        // A lone item takes the whole row rather than leaving half the band
        // bare. Measured against the band, not read off grid-column, so it
        // holds however the rule is expressed.
        loneFullWidth: (() => {
          const items = pg.querySelectorAll('.pager__item');
          if (items.length !== 1) return null;
          return items[0].getBoundingClientRect().width >= pg.getBoundingClientRect().width - 2;
        })(),
        label: pg.getAttribute('aria-label'),
      };
    });
    ok(`${u}: has a pager`, r !== null);
    if (!r) continue;
    ok(`  prev ${wantPrev ? 'present' : 'absent'} / next ${wantNext ? 'present' : 'absent'}`,
       r.prev === wantPrev && r.next === wantNext, JSON.stringify(r));
    ok(`  sits after the content and before the closing band`, r.afterContent && r.beforeCta, JSON.stringify(r));
    ok(`  labelled by its section`, !!r.label, r.label);
    // One link, so it spans the band. This used to expect a lone NEXT pinned to
    // the right cell, which predates the "if one, make it full width" rule —
    // and no page had a lone next until the pager stopped paging up to the
    // category, so the assertion had never actually run.
    if (wantPrev !== wantNext)
      ok(`  the lone link spans the band`, r.loneFullWidth === true, JSON.stringify(r));
  }

  // The rule behind the case above: previous/next walks SIBLINGS. A pager that
  // points at a category overview is pointing up the tree, not along it.
  console.log('\n== no pager link points at a category overview ==');
  {
    const CATEGORY = ['general-dentistry', 'cosmetic-dentistry',
                      'preventative-dentistry', 'missing-teeth', 'treatments'];
    const fs2 = require('fs');
    const leaves = fs2.readdirSync('/home/user/botesdale-dental-clinic/pages')
      .filter(f => f.endsWith('.html')).map(f => 'pages/' + f);
    let seen = 0; const bad = [];
    for (const u of leaves) {
      await go(u);
      const hrefs = await p.evaluate(() =>
        [...document.querySelectorAll('.pager__item')].map(a => a.getAttribute('href')));
      if (!hrefs.length) continue;
      seen++;
      for (const h of hrefs) {
        // Compare the FILENAME, not a suffix: case-replacement-of-missing-teeth
        // ends with "missing-teeth" and is a case study, not the category.
        const file = (h || '').split('/').pop();
        if (CATEGORY.includes(file.replace(/\.html$/, ''))) bad.push(u + ' -> ' + h);
      }
    }
    ok('enough pagers sampled', seen >= 15, 'only ' + seen);
    ok(seen + ' pagers step sideways, never up to a category', bad.length === 0,
       JSON.stringify(bad.slice(0, 6)));
  }

  // hub/overview pages never carried a rail, so they get no pager either.
  // The implant pages are not a sequence — that grouping was invented and has
  // been withdrawn — so they take none either.
  for (const u of ['pages/cosmetic-dentistry.html', 'pages/treatments.html',
                   'pages/implant-clinic.html', 'pages/implant-referrals.html',
                   'pages/missing-teeth.html']) {
    await go(u);
    const has = await p.evaluate(() => !!document.querySelector('.pager'));
    ok(`${u}: correctly has no pager`, !has);
  }

  console.log('\n== header scrim: hero copy can no longer collide with the logo ==');
  const m = await b.newPage({ viewport: { width: 414, height: 800 } });
  await m.route('**://*.google*/**', r => r.abort());
  await m.goto(`http://localhost:8931/pages/case-replacement-of-missing-teeth.html?v=${v}`, { waitUntil: 'networkidle' });
  let worst = null;
  for (const y of [0, 60, 120, 180, 240, 300]) {
    await m.evaluate(sy => window.scrollTo(0, sy), y);
    await m.waitForTimeout(220);
    const r = await m.evaluate(() => {
      const nav = document.querySelector('.nav');
      const s = getComputedStyle(nav, '::before');
      const brand = document.querySelector('.brand').getBoundingClientRect();
      const h1 = document.querySelector('.page-head h1, .hero h1').getBoundingClientRect();
      const overlap = !(h1.bottom < brand.top || h1.top > brand.bottom);
      return { y: Math.round(window.scrollY), scrolled: nav.classList.contains('is-scrolled'),
               scrimOpacity: parseFloat(s.opacity), hasScrim: s.content !== 'none', overlap };
    });
    // wherever the title is behind the header, a scrim must be covering it
    if (r.overlap && !r.scrolled && r.scrimOpacity < 1) worst = r;
  }
  ok('a scrim covers the header whenever hero copy is behind it', worst === null, JSON.stringify(worst));
  const solid = await m.evaluate(async () => {
    window.scrollTo(0, 2000);
    await new Promise(r => setTimeout(r, 400));
    const nav = document.querySelector('.nav');
    return { scrolled: nav.classList.contains('is-scrolled'),
             scrim: parseFloat(getComputedStyle(nav, '::before').opacity) };
  });
  ok('scrim fades out once the header goes solid', solid.scrolled && solid.scrim === 0, JSON.stringify(solid));

  console.log('\n== no overflow / dead styles ==');
  for (const [u, w] of [['pages/crowns.html', 390], ['pages/implant-clinic.html', 390], ['pages/crowns.html', 1400]]) {
    const q = await b.newPage({ viewport: { width: w, height: 900 } });
    await q.route('**://*.google*/**', r2 => r2.abort());
    await q.goto(`http://localhost:8931/${u}?v=${v}`, { waitUntil: 'domcontentloaded' });
    const o = await q.evaluate(() => ({ s: document.documentElement.scrollWidth, i: window.innerWidth }));
    ok(`${u} @${w}: no horizontal overflow`, o.s <= o.i, `${o.s}>${o.i}`);
    await q.close();
  }
  const dead = await p.evaluate(() => {
    let hits = 0;
    for (const sheet of document.styleSheets) {
      let rules; try { rules = sheet.cssRules; } catch { continue; }
      const walk = rs => { for (const r of rs) { if (r.cssRules) walk(r.cssRules);
        else if (r.selectorText && /\.rail|\.with-rail/.test(r.selectorText)) hits++; } };
      walk(rules);
    }
    return hits;
  });
  ok('no rail rules left in the stylesheets', dead === 0, `${dead} rules`);

  await b.close();
  console.log(fail === 0 ? '\nALL PASSED' : `\n${fail} FAILED`);
  process.exit(fail ? 1 : 0);
})();
