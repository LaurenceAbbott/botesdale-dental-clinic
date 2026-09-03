// One running-copy size. The scale had drifted to 17-18px for "lead" copy —
// the hero sub, the paragraph under a section head, .lead — against 16px body,
// which reads as an inconsistency rather than a hierarchy. Running copy is now
// 15px everywhere; intros are distinguished by measure, line-height and colour.
//
// Sweeps every page at three widths. The only paragraph allowed to be larger is
// the statement band, which is a display voice, not something you read through.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = '/home/user/botesdale-dental-clinic';
const pages = ['index.html', '404.html'].concat(
  fs.readdirSync(path.join(ROOT, 'pages')).filter(f => f.endsWith('.html')).map(f => 'pages/' + f));

const BODY_MAX = 15;      // px
const BTN_H    = 48;      // px, +/- 1 for the border and line-box rounding
const BTN_R    = 4;       // px corner radius
let failed = 0;
const fail = m => { console.log('  FAIL  ' + m); failed++; };

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const w of [390, 1024, 1600]) {
    console.log('\n== ' + w + 'px ==');
    const before = failed;
    const ctx = await b.newContext({ viewport: { width: w, height: 900 } });
    const p = await ctx.newPage();
    await p.route('**://*.google*/**', r => r.abort());
    let paras = 0, btns = 0;
    for (const u of pages) {
      const resp = await p.goto('http://127.0.0.1:8931/' + u, { waitUntil: 'domcontentloaded' });
      // A URL that 404s renders the SERVER's error page; measuring that as if
      // it were the site is how a stale page list hides behind a green run.
      if (!resp || resp.status() !== 200) { fail(u + ' returned ' + (resp && resp.status())); continue; }
      const r = await p.evaluate((max) => {
        const over = [], name = e => e.className && typeof e.className === 'string'
          ? e.className.trim().split(/\s+/)[0] : e.tagName.toLowerCase();
        let n = 0;
        for (const e of document.querySelectorAll('p, li, dd, dt')) {
          if (!e.textContent.trim()) continue;
          // Display voices — set in the head font at heading sizes, not read through.
          if (e.closest('.statement, .quote, .label, .meta')) continue;
          if (e.classList.contains('statement-text')) continue;
          n++;
          const px = parseFloat(getComputedStyle(e).fontSize);
          if (px > max + 0.01) over.push({ px, where: name(e.parentElement || e) });
        }
        const bh = [];
        for (const e of document.querySelectorAll('.btn:not(.btn--sm)')) {
          if (e.offsetParent === null) continue;
          bh.push({ h: +e.getBoundingClientRect().height.toFixed(1), t: e.textContent.trim().slice(0, 20) });
        }
        // Buttons are just off square at 4px — softened, not rounded. Every
        // button-shaped control shares it: .btn, the header CTA, the sheet CTA.
        const br = [];
        for (const e of document.querySelectorAll('.btn, .nav__cta, .menu__cta')) {
          if (e.offsetParent === null) continue;
          br.push({ r: parseFloat(getComputedStyle(e).borderTopLeftRadius),
                    t: (e.className || '') + ' ' + e.textContent.trim().slice(0, 16) });
        }
        return { over, n, bh, br };
      }, BODY_MAX);
      paras += r.n; btns += r.bh.length;
      for (const o of r.over)
        fail(u + ' — ' + o.where + ' body copy at ' + o.px + 'px (max ' + BODY_MAX + ')');
      for (const x of r.bh)
        if (Math.abs(x.h - BTN_H) > 1)
          fail(u + ' — button "' + x.t + '" is ' + x.h + 'px tall (want ' + BTN_H + ')');
      for (const x of r.br)
        if (Math.abs(x.r - BTN_R) > 0.5)
          fail(u + ' — button "' + x.t.trim() + '" has a ' + x.r + 'px radius (want ' + BTN_R + ')');
    }
    if (paras < 300) fail('only ' + paras + ' paragraphs seen at ' + w + 'px — the sweep is not reaching them');
    else if (btns < 20) fail('only ' + btns + ' buttons seen at ' + w + 'px');
    else if (failed === before)
      console.log('  PASS  ' + paras + ' paragraphs <= ' + BODY_MAX + 'px, ' + btns + ' buttons at ' + BTN_H + 'px');
    await ctx.close();
  }
  await b.close();
  console.log(failed ? '\n' + failed + ' FAILED' : '\nALL PASSED');
  process.exit(failed ? 1 : 0);
})();
