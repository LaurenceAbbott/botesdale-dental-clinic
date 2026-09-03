// Does the before/after comparison actually work — as a wipe, by pointer and
// by keyboard — and does the tag sit clear of the 32px corner?
const { chromium } = require('playwright');
const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const BASE = 'http://localhost:8931';

const PAGES = [
  ['/index.html', 'home'],
  ['/pages/case-treating-worn-dentition.html', 'case-worn'],
  ['/pages/case-same-day-teeth.html', 'case-sameday'],
  ['/pages/style-guide.html', 'style-guide'],
];

let fails = 0;
const bad = (m) => { fails++; console.log('  FAIL ' + m); };
const ok = (m) => console.log('  ok   ' + m);

(async () => {
  const browser = await chromium.launch({ executablePath: EXE });

  for (const [path, name] of PAGES) {
    for (const vp of [{ width: 1280, height: 900, tag: 'desktop' },
                      { width: 390, height: 844, tag: 'mobile' }]) {
      const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
      const page = await ctx.newPage();
      await page.route('**://*.google*/**', r => r.abort());
      const errs = [];
      page.on('pageerror', e => errs.push(e.message));
      await page.goto(BASE + path, { waitUntil: 'networkidle' });
      console.log(`\n${name} @ ${vp.tag}`);

      if (errs.length) bad('JS errors: ' + errs.join(' | '));

      const n = await page.locator('.compare').count();
      if (n === 0) { bad('no .compare on this page'); await ctx.close(); continue; }
      ok(`${n} comparison(s)`);

      const c = page.locator('.compare').first();
      await c.scrollIntoViewIfNeeded();

      // 1. JS published --pos.
      const pos0 = await c.evaluate(el => el.style.getPropertyValue('--pos'));
      if (pos0 !== '50%') bad(`--pos not initialised (got "${pos0}")`); else ok('--pos = 50%');

      // 2. The before pane is clipped to half the frame, and it is CLIPPED —
      //    not resized — so the photograph underneath is uncovered rather
      //    than re-cropped.
      const geo = await c.evaluate(el => {
        const f = el.getBoundingClientRect();
        const b = el.querySelector('.compare__pane--before').getBoundingClientRect();
        const cs = getComputedStyle(el.querySelector('.compare__pane--before'));
        return { fw: f.width, fh: f.height, bw: b.width, clip: cs.clipPath, r: getComputedStyle(el).borderTopLeftRadius };
      });
      if (Math.abs(geo.bw - geo.fw) > 1) bad(`before pane resized (${geo.bw} vs frame ${geo.fw})`);
      else ok('before pane is full width, clipped not resized');
      if (!/inset/.test(geo.clip)) bad('no clip-path on the before pane: ' + geo.clip);
      if (geo.r !== '32px') bad('frame radius is ' + geo.r); else ok('frame radius 32px');

      // 3. Dragging the range moves the divider and the clip.
      const box = await c.boundingBox();
      await page.mouse.move(box.x + box.width * 0.5, box.y + box.height * 0.5);
      await page.mouse.down();
      await page.mouse.move(box.x + box.width * 0.8, box.y + box.height * 0.5, { steps: 8 });
      await page.mouse.up();
      const after = await c.evaluate(el => {
        const f = el.getBoundingClientRect();
        const l = el.querySelector('.compare__line').getBoundingClientRect();
        return { pos: el.style.getPropertyValue('--pos'), frac: (l.left + l.width / 2 - f.left) / f.width };
      });
      const pct = parseFloat(after.pos);
      if (!(pct > 70 && pct < 90)) bad(`drag to 80% left --pos at ${after.pos}`);
      else ok(`drag moved --pos to ${after.pos}`);
      if (Math.abs(after.frac - pct / 100) > 0.02) bad(`divider at ${(after.frac * 100).toFixed(1)}% but --pos ${after.pos}`);
      else ok('divider tracks --pos');

      // 4. Keyboard.
      await c.locator('.compare__range').focus();
      const beforeKey = parseFloat(await c.evaluate(el => el.style.getPropertyValue('--pos')));
      await page.keyboard.press('ArrowLeft');
      await page.keyboard.press('ArrowLeft');
      const afterKey = parseFloat(await c.evaluate(el => el.style.getPropertyValue('--pos')));
      if (afterKey >= beforeKey) bad(`arrow keys did not move --pos (${beforeKey} -> ${afterKey})`);
      else ok(`arrow keys move --pos (${beforeKey} -> ${afterKey})`);

      // 5. Accessible name on the control.
      const label = await c.locator('.compare__range').getAttribute('aria-label');
      if (!label) bad('range has no accessible name'); else ok('range is named');

      // 6. Tags: at the bottom centre, flanking the middle, clear of the
      //    32px corner curve and of each other.
      const tags = await c.evaluate(el => {
        const f = el.getBoundingClientRect();
        const t = [...el.querySelectorAll('.compare__tag')].map(x => {
          const r = x.getBoundingClientRect();
          return { cls: x.className, l: r.left - f.left, r: f.right - r.right,
                   b: f.bottom - r.bottom, w: r.width, visible: getComputedStyle(x).visibility };
        });
        return { fw: f.width, t };
      });
      const bt = tags.t.find(x => /--before/.test(x.cls));
      const at = tags.t.find(x => /--after/.test(x.cls));
      if (!bt || !at) bad('missing a tag');
      else {
        if (bt.b < 8 || at.b < 8) bad(`tag flush to the bottom edge (${bt.b}/${at.b}px)`);
        else ok(`tags ${bt.b.toFixed(0)}px off the bottom`);
        const gap = (at.l) - (bt.l + bt.w);
        if (gap < 4) bad(`tags overlap (gap ${gap.toFixed(1)}px)`);
        else ok(`tags flank the centre, ${gap.toFixed(0)}px apart`);
        // The axis is the GAP between them — i.e. the divider's rest
        // position — not the pair's bounding box: "Before" and "After" are
        // different widths, so centring the box would push the gap off centre.
        const mid = tags.fw / 2;
        const gapMid = (bt.l + bt.w + at.l) / 2;
        if (Math.abs(gapMid - mid) > 1) bad(`gap between tags not on the centre line (${gapMid.toFixed(1)} vs ${mid.toFixed(1)})`);
        else ok('gap between tags sits on the centre line');
        // Corner clearance: the tag must not intrude on the 32px curve.
        if (bt.l < 24 && bt.b < 24) bad('before tag sits inside the corner curve');
      }

      // 7. The grip is on top of the panes and centred on the divider.
      const grip = await c.evaluate(el => {
        const l = el.querySelector('.compare__line').getBoundingClientRect();
        const g = el.querySelector('.compare__grip').getBoundingClientRect();
        return { dx: (g.left + g.width / 2) - (l.left + l.width / 2), w: g.width };
      });
      if (Math.abs(grip.dx) > 1) bad(`grip off the divider by ${grip.dx.toFixed(1)}px`);
      else ok(`grip centred, ${grip.w}px`);
      if (grip.w < 40) bad(`grip only ${grip.w}px — under the 44px touch target`);

      // 8. A vertical swipe over the comparison must still scroll the page.
      const ta = await c.locator('.compare__range').evaluate(el => getComputedStyle(el).touchAction);
      if (!/pan-y/.test(ta)) bad('touch-action is ' + ta + ' — a vertical swipe would be swallowed');
      else ok('vertical swipe still scrolls');

      // 9. The page must not scroll sideways.
      const ow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      if (ow > 1) bad(`horizontal overflow of ${ow}px`); else ok('no sideways scroll');

      await ctx.close();
    }
  }

  // 10. The old corner tag is gone everywhere.
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  await page.route('**://*.google*/**', r => r.abort());
  await page.goto(BASE + '/pages/case-same-day-teeth.html', { waitUntil: 'networkidle' });
  console.log('\nshot tags');
  const shots = await page.evaluate(() => [...document.querySelectorAll('.shot__tag')].map(t => {
    const f = t.closest('.shot').getBoundingClientRect(), r = t.getBoundingClientRect();
    return { off: (r.left + r.width / 2 - f.left) - f.width / 2, b: f.bottom - r.bottom,
             rad: getComputedStyle(t).borderTopLeftRadius };
  }));
  if (!shots.length) bad('no .shot__tag to check');
  shots.forEach((s, i) => {
    if (Math.abs(s.off) > 1.5) bad(`shot tag ${i} not centred (${s.off.toFixed(1)}px off)`);
    if (s.b < 8) bad(`shot tag ${i} flush to the bottom (${s.b}px)`);
    if (s.rad !== '4px') bad(`shot tag ${i} radius ${s.rad}`);
  });
  if (shots.length) ok(`${shots.length} shot tag(s) centred, off the edge, 4px`);
  await ctx.close();

  await browser.close();
  console.log(fails ? `\n${fails} FAILURE(S)` : '\nALL PASS');
  process.exit(fails ? 1 : 0);
})();
