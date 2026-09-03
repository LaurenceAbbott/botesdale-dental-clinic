// A hover state is a promise that the thing under the cursor does something.
//
// Three containers broke that promise: .card (which styled the <article> form
// as well as the <a> one), .strip__item (same), and .plan on the fees page,
// which is a price card you read and has never been a link. On iOS it is
// worse than a false affordance — :hover sticks after a tap, so the tile sits
// there looking selected.
//
// This hovers each container that is NOT a link and asserts nothing inside it
// repaints. Links inside it may still react; that is the point of putting the
// link there.
//
// Two things this has to do that a first-draft version did not, both found by
// negative-testing rather than by reading it:
//   - Check EVERY match, not just the first. .plan--feature already carries a
//     black border, so restoring `.plan:hover { border-color: black }` is a
//     no-op on the first card on the page and the guard sailed past it.
//   - Watch the whole subtree, not just the element. The strip's rule was
//     `.strip__item:hover .strip__media { background: ... }` — it repaints a
//     CHILD, and reading only the tile's own computed style missed it.
const { chromium } = require('playwright');
const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const BASE = 'http://localhost:8931';

// Containers that are laid out like something clickable but are not.
// needsLink: a tile that stands in for a page must still lead there. A price
// card is informational and legitimately has no control, so it is exempt —
// asserting otherwise just makes the guard cry wolf.
const TARGETS = [
  ['/index.html', '.card--static', 'home page case card', true],
  ['/pages/case-studies.html', '.strip__item--static', 'case studies index tile', true],
  ['/pages/fees-and-membership.html', '.plan', 'fees plan card', false],
  ['/pages/fees-and-membership.html', '.plan--feature', 'fees feature plan card', false],
];

// What the eye reads as "this reacts to you".
const PROPS = ['borderTopColor', 'borderLeftColor', 'backgroundColor', 'transform',
               'boxShadow', 'opacity', 'outlineColor'];

let fails = 0;
const bad = (m) => { fails++; console.log('  FAIL ' + m); };
const ok = (m) => console.log('  ok   ' + m);

(async () => {
  const browser = await chromium.launch({ executablePath: EXE });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  await page.route('**://*.google*/**', r => r.abort());

  for (const [path, sel, label, needsLink] of TARGETS) {
    await page.goto(BASE + path, { waitUntil: 'networkidle' });
    console.log('\n' + label + '  (' + sel + ')');

    const n = await page.locator(sel).count();
    if (!n) { bad(`no ${sel} on ${path} — the fixture has moved`); continue; }

    ok(`${n} to check`);

    for (let i = 0; i < n; i++) {
      const el = page.locator(sel).nth(i);
      await el.scrollIntoViewIfNeeded();

      // It must not be a link, or the whole premise is wrong.
      const interactive = await el.evaluate(e =>
        e.tagName === 'A' || e.tagName === 'BUTTON' || !!e.closest('a, button'));
      if (interactive) { bad(`${sel}[${i}] IS clickable — this check points at the wrong thing`); continue; }

      // The element AND everything under it: a hover rule commonly repaints a
      // child rather than the hovered box.
      const read = () => el.evaluate((e, props) => {
        return [e, ...e.querySelectorAll('*')].map(node => {
          const cs = getComputedStyle(node);
          const o = { tag: node.tagName, cls: node.className.toString().split(' ')[0] };
          props.forEach(p => { o[p] = cs[p]; });
          return o;
        });
      }, PROPS);

      // Park the pointer well away and let the scroll-in animation finish
      // first: [data-reveal] is still moving opacity and transform for ~.6s
      // after the tile enters view, and reading through it reports a "hover
      // change" that is nothing of the kind.
      await page.mouse.move(2, 2);
      await el.evaluate(e => {
        (e.closest('[data-reveal]') || e).classList.add('is-in');
        e.querySelectorAll('[data-reveal]').forEach(x => x.classList.add('is-in'));
      });
      await page.waitForTimeout(900);
      const before = await read();
      await el.hover();
      await page.waitForTimeout(400);   // past --t-fast / --t
      const after = await read();

      let moved = 0;
      before.forEach((b, j) => {
        const a = after[j];
        if (!a) return;
        PROPS.forEach(prop => {
          if (b[prop] !== a[prop]) {
            moved++;
            const who = b === before[0] ? sel : `${sel} > .${b.cls || b.tag.toLowerCase()}`;
            bad(`${who} [${i}] changes ${prop} on hover: ${b[prop]} -> ${a[prop]}`);
          }
        });
      });
      if (!moved) ok(`[${i}] nothing in it repaints on hover`);

      if (needsLink) {
        const links = await el.evaluate(e => e.querySelectorAll('a[href]').length);
        if (!links) bad(`${sel}[${i}] has no link inside it — it is now a dead end`);
        else ok(`[${i}] ${links} real link(s) inside it`);
      }
    }
  }

  await browser.close();
  console.log(fails ? `\n${fails} FAILURE(S)` : '\nALL PASS');
  process.exit(fails ? 1 : 0);
})();
