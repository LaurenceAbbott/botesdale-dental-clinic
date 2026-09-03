const { chromium } = require('playwright');
const fs = require('fs');
let fail = 0;
const ok = (n, c, x = '') => { console.log(`${c ? '  PASS' : '  FAIL'}  ${n}${c ? '' : '  << ' + x}`); if (!c) fail++; };
const lin = c => (c /= 255) <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
const L = ([r, g, bl]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(bl);
const CR = (a, b) => { const la = L(a), lb = L(b); return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05); };
const px = s => s.match(/[\d.]+/g).map(Number);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  await p.route('**://*.google*/**', r => r.abort());
  const pages = ['index.html', ...fs.readdirSync('/home/user/botesdale-dental-clinic/pages')
    .filter(f => f.endsWith('.html')).map(f => 'pages/' + f)];

  const invisible = [], styles = new Set(), lowContrast = [], plainPhones = [];
  for (const u of pages) {
    await p.goto(`http://localhost:8931/${u}`, { waitUntil: 'domcontentloaded' });
    const r = await p.evaluate(() => {
      const CHROME = '.nav,.menu,.footer,.pager,.tabs,.crumbs,.cookie,.btn,.arc-link,.card,.strip,.skip-link,.to-top,.chooser,.sg-';
      const out = { links: [], plainPhone: false };
      for (const a of document.querySelectorAll('a')) {
        if (a.closest(CHROME) || a.matches(CHROME)) continue;
        if (!a.closest('p, li, dd, td, .prose, .legal, .notice, .section-head')) continue;
        const s = getComputedStyle(a);
        // nearest painted background
        let n = a, bg = 'rgba(0, 0, 0, 0)';
        while (n && n !== document.documentElement) {
          const c = getComputedStyle(n).backgroundColor;
          if (c && !/rgba\(0, 0, 0, 0\)/.test(c)) { bg = c; break; }
          n = n.parentElement;
        }
        out.links.push({ cls: a.className || '(none)', color: s.color,
          pc: getComputedStyle(a.parentElement).color, deco: s.textDecorationLine,
          bw: s.borderBottomWidth, bc: s.borderBottomColor, bg, text: a.textContent.trim().slice(0, 24) });
      }
      // a bare phone number left as text anywhere in copy
      const wanted = '01379 897176';
      for (const el of document.querySelectorAll('p, li, dd')) {
        if (el.closest('.footer, .nav, .menu')) continue;
        if (el.textContent.includes(wanted) && !el.querySelector('a[href^="tel:"]')) out.plainPhone = true;
      }
      return out;
    });
    if (r.plainPhone) plainPhones.push(u);
    for (const l of r.links) {
      if (l.color === l.pc && l.deco === 'none' && parseFloat(l.bw) === 0)
        invisible.push(`${u}: "${l.text}"`);
      styles.add(`${l.color}|${l.deco}|${l.bw}|${l.bc}`);
      const fg = px(l.color).slice(0, 3), bgc = px(l.bg).slice(0, 3);
      if (bgc.length === 3) {
        const cr = CR(fg, bgc);
        if (cr < 4.5) lowContrast.push(`${u}: "${l.text}" ${cr.toFixed(2)}:1 (${l.color} on ${l.bg})`);
      }
    }
  }

  console.log('\n== link styling ==');
  ok('no link in running copy is indistinguishable from its text', invisible.length === 0,
     JSON.stringify([...new Set(invisible)].slice(0, 6)));
  ok('inline links share one computed treatment per ground', styles.size <= 2,
     `${styles.size} distinct: ${JSON.stringify([...styles])}`);
  ok('every inline link clears AA against its ground', lowContrast.length === 0,
     JSON.stringify([...new Set(lowContrast)].slice(0, 6)));

  console.log('\n== the phone number ==');
  ok('never left as plain text in copy for iOS to auto-style', plainPhones.length === 0,
     JSON.stringify(plainPhones));
  await p.goto('http://localhost:8931/pages/crowns.html', { waitUntil: 'domcontentloaded' });
  const tel = await p.evaluate(() => {
    const a = document.querySelector('.cta a[href^="tel:"]');
    if (!a) return null;
    const s = getComputedStyle(a);
    return { cls: a.className, href: a.getAttribute('href'),
             border: s.borderBottomWidth, color: s.color };
  });
  ok('CTA phone is a real tel: link', tel && /^tel:\+44/.test(tel.href), JSON.stringify(tel));
  ok('and carries the site inline-link styling', tel && parseFloat(tel.border) > 0, JSON.stringify(tel));
  const meta = await p.evaluate(() => {
    const m = document.querySelector('meta[name="format-detection"]');
    return m && m.getAttribute('content');
  });
  ok('format-detection stops iOS auto-linking anything else', meta === 'telephone=no', String(meta));

  console.log('\n== the previously invisible one ==');
  await p.goto('http://localhost:8931/pages/contact-us.html', { waitUntil: 'domcontentloaded' });
  const notice = await p.evaluate(() => {
    const a = document.querySelector('.notice a[href^="tel:"]');
    if (!a) return null;
    const s = getComputedStyle(a);
    return { border: s.borderBottomWidth, color: s.color,
             parent: getComputedStyle(a.parentElement).color };
  });
  ok('contact-us notice tel: link is now visible as a link',
     notice && (parseFloat(notice.border) > 0 || notice.color !== notice.parent), JSON.stringify(notice));

  // Every inline link, measured against the ground it actually sits on. The
  // dark-ground rule in base.css is a hand-maintained list of contexts
  // (.section--dark, .statement, .cta--dark, ...) and every new dark surface
  // has to be added to it. .split-card__copy was missed exactly that way, and
  // --accent-700 on --black is 2.4:1: an underline with nothing legible above
  // it. A list you must remember to extend is not a guarantee; this is.
  {
    const bad = [];
    let checked = 0;
    for (const u of pages) {
      const resp = await p.goto(`http://localhost:8931/${u}`, { waitUntil: 'domcontentloaded' });
      if (!resp || resp.status() !== 200) { bad.push(u + ' -> HTTP ' + (resp && resp.status())); continue; }
      const rows = await p.evaluate(() => {
        const px = t => t.match(/[\d.]+/g).map(Number);
        // Walk up for the first ancestor that actually paints a background.
        const groundOf = el => {
          let n = el;
          while (n && n !== document.documentElement) {
            const bg = px(getComputedStyle(n).backgroundColor || 'rgba(0,0,0,0)');
            if (bg.length < 4 || bg[3] > 0.95) return bg.slice(0, 3);
            n = n.parentElement;
          }
          return [247, 246, 243];
        };
        const out = [];
          // The whole inline-link surface base.css turns on, plus every dark
        // panel that carries copy — not a hand-picked few.
        const SEL = ['.link-inline',
          '.prose', '.legal', '.notice', '.specs', '.table', '.cta p', '.statement p',
          '.section-head p', '.form__note', '.field__hint', '.split-card__copy',
          '.intro-center', '.ed__text', '.plan', '.quote'
        ].map(x => x === '.link-inline' ? x : x + ' a:not([class])').join(',');
        for (const a of document.querySelectorAll(SEL)) {
          if (a.offsetParent === null) continue;
          out.push({ fg: px(getComputedStyle(a).color).slice(0, 3), bg: groundOf(a),
                     text: a.textContent.trim().slice(0, 22),
                     where: (a.closest('[class]') || a).className.split(/\s+/)[0] });
        }
        return out;
      });
      for (const r of rows) {
        checked++;
        const ratio = CR(r.fg, r.bg);
        if (ratio < 4.5) bad.push(u + ' — "' + r.text + '" in .' + r.where + ' is ' + ratio.toFixed(2) + ':1');
      }
    }
    console.log('\n== inline links against the ground they sit on ==');
    if (checked < 10) ok('enough inline links sampled', false, 'only ' + checked);
    else ok(checked + ' inline links all clear 4.5:1', bad.length === 0, JSON.stringify(bad.slice(0, 6)));
  }

  await b.close();
  

console.log(fail === 0 ? '\nALL PASSED' : `\n${fail} FAILED`);
  process.exit(fail ? 1 : 0);
})();
