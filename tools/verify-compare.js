// Does the before/after comparison actually work — by mouse, by TOUCH and by
// keyboard — and do the labels sit where the pattern puts them?
//
// The touch case is here because it is the one that shipped broken: the
// native range took the drag, which works with a mouse but on iOS only jumps
// on tap, so the comparison could not be dragged on a phone at all. A test
// that only drives page.mouse would have stayed green through that.
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

      // 3. Mouse: press and drag moves the divider and the clip with it.
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

      // 3b. TOUCH: a real pointerType 'touch' drag has to move it too, and
      //     it must move on the DRAG, not on the initial contact — the first
      //     touch of a vertical scroll must not yank the divider sideways.
      const touch = await c.evaluate(el => {
        const r = el.getBoundingClientRect();
        const y = r.top + r.height / 2;
        const ev = (type, x) => el.dispatchEvent(new PointerEvent(type, {
          bubbles: true, cancelable: true, pointerId: 7, pointerType: 'touch',
          isPrimary: true, clientX: x, clientY: y }));
        const read = () => parseFloat(el.style.getPropertyValue('--pos'));
        el.querySelector('.compare__range').value = 50; 
        el.style.setProperty('--pos', '50%');
        // Press somewhere OTHER than the current 50%, or a jump-on-contact
        // regression lands on the value that was already there and hides.
        ev('pointerdown', r.left + r.width * 0.8);
        const onDown = read();
        ev('pointermove', r.left + r.width * 0.22);
        const onMove = read();
        ev('pointerup', r.left + r.width * 0.22);
        return { onDown, onMove };
      });
      if (Math.abs(touch.onMove - 22) > 3) bad(`touch drag to 22% left --pos at ${touch.onMove}%`);
      else ok(`touch drag moved --pos to ${touch.onMove.toFixed(0)}%`);
      if (touch.onDown !== 50) bad(`touch contact alone moved --pos to ${touch.onDown}% — a vertical scroll would yank the divider`);
      else ok('touch contact alone does not move it');

      // 3c. The input must not be the pointer target — that is what broke on
      //     iOS. Whatever is under the middle of the frame has to be the
      //     frame or its own decoration, never the range.
      const hit = await c.evaluate(el => {
        const r = el.getBoundingClientRect();
        const t = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
        return t ? t.className.toString() : 'none';
      });
      if (/compare__range/.test(hit)) bad('the range input is the pointer target — drag will not work on iOS');
      else ok('the frame takes the pointer, not the range');

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

      // 6. Labels: each pinned to the outer corner of the half it names,
      //    inset far enough to clear the 32px curve.
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
      if (!bt || !at) bad('missing a label');
      else {
        if (bt.b < 8 || at.b < 8) bad(`label flush to the bottom edge (${bt.b}/${at.b}px)`);
        else ok(`labels ${bt.b.toFixed(0)}px off the bottom`);
        if (Math.abs(bt.l - 16) > 1) bad(`before label ${bt.l.toFixed(1)}px from the left, want 16`);
        else if (Math.abs(at.r - 16) > 1) bad(`after label ${at.r.toFixed(1)}px from the right, want 16`);
        else ok('labels in the outer corners, 16px in');
        // The 32px curve reaches sqrt(2)*(32-d) from the corner centre; at a
        // 16px inset that is 22.6px, inside the 32px radius. Assert the real
        // geometry rather than the number, so a change to --radius-media is
        // caught rather than silently clipping a corner off a label.
        const rad = 32, d = Math.min(bt.l, bt.b);
        if (Math.hypot(rad - d, rad - d) > rad) bad(`label intrudes on the ${rad}px curve at a ${d}px inset`);
        else ok('labels clear the corner curve');
        // They must not collide across the middle at any width.
        if (bt.l + bt.w > at.l) bad('labels overlap');
        else ok(`${(at.l - bt.l - bt.w).toFixed(0)}px between them`);
      }

      // 6b. A label whose side has shrunk past it gets out of the way, rather
      //     than sitting over the other photograph and mislabelling it.
      const fade = await c.evaluate(async el => {
        const range = el.querySelector('.compare__range');
        const wait = ms => new Promise(r => setTimeout(r, ms));
        // Past the .18s transition — reading opacity the instant the class
        // lands returns the value it is animating FROM, not to.
        const set = async v => {
          range.value = v;
          range.dispatchEvent(new Event('input', { bubbles: true }));
          await wait(320);
        };
        const read = () => ({
          b: getComputedStyle(el.querySelector('.compare__tag--before')).opacity,
          a: getComputedStyle(el.querySelector('.compare__tag--after')).opacity,
          bc: el.querySelector('.compare__tag--before').classList.contains('is-gone'),
          ac: el.querySelector('.compare__tag--after').classList.contains('is-gone'),
        });
        await set(2);  const lo = read();
        await set(98); const hi = read();
        await set(50); const mid = read();
        return { lo, hi, mid };
      });
      if (!fade.lo.bc || !fade.hi.ac) bad('the is-gone class does not track the divider');
      else if (fade.lo.b !== '0') bad(`before label still shown with the before image gone (opacity ${fade.lo.b})`);
      else if (fade.hi.a !== '0') bad(`after label still shown with the after image gone (opacity ${fade.hi.a})`);
      else if (fade.mid.b !== '1' || fade.mid.a !== '1') bad(`a label is hidden at rest (${fade.mid.b}/${fade.mid.a})`);
            else ok('each label steps aside once its own side is gone');

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
      const ta = await c.evaluate(el => getComputedStyle(el).touchAction);
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
