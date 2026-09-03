// What does the top scrim ACTUALLY need, row by row?
// Hides both scrims, screenshots the bare photograph, then for every scanline
// under the header works out the minimum alpha that keeps the elements sitting
// on that row at their required ratio. The answer is a curve; the gradient
// only has to stay above it.
const { chromium } = require('playwright');
const zlib = require('zlib');

function decodePNG(buf) {
  let o = 8, w = 0, h = 0, ct = 0, idat = [];
  while (o < buf.length) {
    const len = buf.readUInt32BE(o), type = buf.toString('ascii', o + 4, o + 8);
    const data = buf.slice(o + 8, o + 8 + len);
    if (type === 'IHDR') { w = data.readUInt32BE(0); h = data.readUInt32BE(4); ct = data[9]; }
    else if (type === 'IDAT') idat.push(data);
    else if (type === 'IEND') break;
    o += 12 + len;
  }
  const raw = zlib.inflateSync(Buffer.concat(idat));
  const bpp = ct === 6 ? 4 : 3, stride = w * bpp;
  const out = Buffer.alloc(h * stride);
  let p = 0;
  for (let y = 0; y < h; y++) {
    const f = raw[p++]; const line = raw.slice(p, p + stride); p += stride;
    for (let x = 0; x < stride; x++) {
      const a = x >= bpp ? out[y * stride + x - bpp] : 0;
      const b = y > 0 ? out[(y - 1) * stride + x] : 0;
      const c = (x >= bpp && y > 0) ? out[(y - 1) * stride + x - bpp] : 0;
      let v = line[x];
      if (f === 1) v += a; else if (f === 2) v += b; else if (f === 3) v += (a + b) >> 1;
      else if (f === 4) { const pa = Math.abs(b - c), pb = Math.abs(a - c), pc = Math.abs(a + b - 2 * c);
        v += (pa <= pb && pa <= pc) ? a : (pb <= pc ? b : c); }
      out[y * stride + x] = v & 255;
    }
  }
  return { w, h, bpp, stride, data: out };
}
const lin = c => (c /= 255) <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
const L = c => 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2]);
const CR = (a, b) => { const la = L(a), lb = L(b); return (Math.max(la, lb) + .05) / (Math.min(la, lb) + .05); };
const over = (fg, a, bg) => [0, 1, 2].map(i => a * fg[i] + (1 - a) * bg[i]);
const INK = [26, 26, 24];
const PAPER = [247, 246, 243];

// Minimum scrim alpha so `fgAlpha`-translucent paper on this pixel clears `need`.
function minAlpha(pixel, fgAlpha, need) {
  for (let a = 0; a <= 1.0001; a += 0.005) {
    const ground = over(INK, a, pixel);
    const text = over(PAPER, fgAlpha, ground);
    if (CR(text, ground) >= need) return a;
  }
  return null;                                   // unreachable at any alpha
}

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const w of [1440, 390]) {
    console.log('\n================ ' + w + 'px ================');
    const ctx = await b.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 });
    const p = await ctx.newPage();
    await p.route('**://*.google*/**', r => r.abort());
    await p.goto('http://127.0.0.1:8931/pages/about-us.html', { waitUntil: 'networkidle' });
    await p.waitForTimeout(500);

    const info = await p.evaluate(() => {
      const head = document.querySelector('.page-head');
      const rect = el => { if (!el || el.offsetParent === null) return null;
        const r = el.getBoundingClientRect();
        return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; };
      const alpha = el => { if (!el) return null;
        const m = getComputedStyle(el).color.match(/[\d.]+/g).map(Number);
        return m.length > 3 ? m[3] : 1; };
      const link = document.querySelector('.page-head__top .crumbs a');
      const cur  = document.querySelector('.page-head__top .crumbs [aria-current]');
      const nav  = document.querySelector('.nav__links a');
      const cta  = document.querySelector('.nav__cta');
      const mark = document.querySelector('.nav__brand');
      const burger = document.querySelector('.nav__burger, .burger, [class*="burger"]');
      const out = {
        headH: Math.round(head.getBoundingClientRect().height),
        items: [
          ['crumb link', rect(link), alpha(link), 4.5],
          ['crumb current', rect(cur), alpha(cur), 4.5],
          ['nav link', rect(nav), alpha(nav), 4.5],
          ['nav cta', rect(cta), alpha(cta), 4.5],
          ['wordmark', rect(mark), 1, 3],
          ['burger', rect(burger), 1, 3],
        ].filter(i => i[1])
      };
      // Hide every scrim so the screenshot is the bare photograph.
      const s = document.createElement('style');
      s.textContent = '.nav::before{display:none!important}.page-head__scrim{display:none!important}' +
                      '.page-head__inner,.nav__inner{visibility:hidden!important}';
      document.head.appendChild(s);
      return out;
    });
    await p.waitForTimeout(300);
    const img = decodePNG(await p.locator('.page-head').screenshot());
    const at = (x, y) => { const i = y * img.stride + x * img.bpp; return [img.data[i], img.data[i+1], img.data[i+2]]; };

    console.log('head is ' + info.headH + 'px tall\n');
    for (const [name, r, fgA, need] of info.items) {
      // The lightest pixel under the element is the worst case.
      let worst = null, wl = -1;
      for (let y = r.y; y < r.y + r.h && y < img.h; y++)
        for (let x = r.x; x < r.x + r.w && x < img.w; x++) {
          const c = at(x, y), l = L(c);
          if (l > wl) { wl = l; worst = c; }
        }
      const a = minAlpha(worst, fgA, need);
      console.log(
        (name + '            ').slice(0, 15) +
        'y ' + String(r.y).padStart(3) + '-' + String(r.y + r.h).padStart(3) +
        '  paper@' + fgA.toFixed(2) +
        '  needs ' + need + ':1  over rgb(' + worst.map(Math.round).join(',') + ')' +
        '  ->  min scrim ' + (a === null ? 'IMPOSSIBLE' : a.toFixed(3)));
    }
    await ctx.close();
  }
  await b.close();
})();
