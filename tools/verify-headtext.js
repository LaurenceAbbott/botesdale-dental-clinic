// Contrast for the crumbs as the EYE sees them, not as a flat average.
//
// The crumbs sit highest in the page head, where the header scrim has eased
// off, so they read straight onto sky. A shadow fixes that locally instead of
// spending more scrim across the whole picture — but a shadow is invisible to
// the usual "text colour vs background colour" check, because the background
// it darkens is only the few pixels touching each glyph.
//
// So: screenshot the crumb row, classify every pixel as glyph or ground, then
// take the LIGHTEST ground pixel that is within 2px of a glyph — the worst
// thing any letter is actually seen against — and measure against that.
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
const PAPER = [247, 246, 243];

// Every piece of page-head copy, with the ratio its size demands. The crumbs
// are the ones that broke, but the flaw — assuming text paints at its declared
// colour — was never specific to them.
const TARGETS = [
  ['crumbs', '.page-head--shot .page-head__top .crumbs', 4.5],
  ['label',  '.page-head--shot .label',                  4.5],
  ['h1',     '.page-head--shot h1',                      3.0],   // large text
  ['sub',    '.page-head--shot .page-head__title p',     4.5],
];
let failed = 0;
const fail = m => { console.log('  FAIL  ' + m); failed++; };

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const w of [390, 1440]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 2 });
    const p = await ctx.newPage();
    await p.route('**://*.google*/**', r => r.abort());
    await p.goto('http://127.0.0.1:8931/pages/about-us.html', { waitUntil: 'networkidle' });
    await p.waitForTimeout(500);

    for (const [name, sel, MIN] of TARGETS) {
      // Screenshot the ELEMENT, not a page-coordinate clip. A clip computed
      // from getBoundingClientRect drifted off the row and quietly sampled
      // plain sky, which read as "no glyphs found" rather than as a wrong
      // measurement.
      const el = await p.$(sel);
      if (!el) { fail(w + 'px — ' + name + ' (' + sel + ') not found'); continue; }
      const img = decodePNG(await el.screenshot());
      const at = (x, y) => { const i = y * img.stride + x * img.bpp; return [img.data[i], img.data[i+1], img.data[i+2]]; };

      let lo = 1, hi2 = 0;
      for (let y = 0; y < img.h; y++) for (let x = 0; x < img.w; x++) {
        const l = L(at(x, y)); if (l < lo) lo = l; if (l > hi2) hi2 = l;
      }
      const cut = lo + (hi2 - lo) * 0.6;
      const isGlyph = [];
      for (let y = 0; y < img.h; y++) { isGlyph[y] = [];
        for (let x = 0; x < img.w; x++) isGlyph[y][x] = L(at(x, y)) >= cut; }

      const BIG = 1e6, dist = [];
      for (let y = 0; y < img.h; y++) { dist[y] = [];
        for (let x = 0; x < img.w; x++) dist[y][x] = isGlyph[y][x] ? 0 : BIG; }
      for (let y = 0; y < img.h; y++) for (let x = 0; x < img.w; x++) {
        let d = dist[y][x];
        if (y > 0) d = Math.min(d, dist[y-1][x] + 1);
        if (x > 0) d = Math.min(d, dist[y][x-1] + 1);
        dist[y][x] = d;
      }
      for (let y = img.h - 1; y >= 0; y--) for (let x = img.w - 1; x >= 0; x--) {
        let d = dist[y][x];
        if (y < img.h - 1) d = Math.min(d, dist[y+1][x] + 1);
        if (x < img.w - 1) d = Math.min(d, dist[y][x+1] + 1);
        dist[y][x] = d;
      }

      // Ground is sampled in a RING, 2-5 CSS px from the nearest glyph.
      // Closer and the pixel is antialiasing — a partly-covered letter, which
      // is bright because it IS the letter; reading that as background is how
      // this check first "measured" a 1.61:1 that did not exist. Further out
      // and a text-shadow's influence has gone, so a shadow would look like it
      // did nothing. The ring is the surface the eye compares against.
      const DSF = 2, NEAR = 2 * DSF, FAR = 5 * DSF;
      let worst = null, wl = -1, near = 0;
      for (let y = 0; y < img.h; y++) for (let x = 0; x < img.w; x++) {
        const d = dist[y][x];
        if (d < NEAR || d > FAR) continue;
        near++;
        const c = at(x, y), l = L(c);
        if (l > wl) { wl = l; worst = c; }
      }
      // The glyph as RENDERED, never as declared. A scrim painting ABOVE the
      // copy darkens the letters too — that is exactly how a 1.68:1 crumb row
      // got reported as 5.36:1, by hiding the text and assuming it would land
      // at full paper.
      let lit = null, ll = -1;
      for (let y = 0; y < img.h; y++) for (let x = 0; x < img.w; x++) {
        if (!isGlyph[y][x]) continue;
        const c = at(x, y), l = L(c);
        if (l > ll) { ll = l; lit = c; }
      }
      if (near < 150 || !lit) { fail(w + 'px ' + name + ' — only ' + near + ' ring px / no glyphs; sample too small to trust'); continue; }

      const declared = await el.evaluate(e => getComputedStyle(e).color);
      const dm = declared.match(/[\d.]+/g).map(Number);
      const declaredRatio = CR(dm.slice(0, 3), worst);
      const ratio = CR(lit, worst);
      const line = w + 'px ' + (name + '      ').slice(0, 7) +
                   ' glyph rgb(' + lit.map(Math.round).join(',') + ') on ground rgb(' +
                   worst.map(Math.round).join(',') + ') = ' + ratio.toFixed(2) + ':1';
      if (ratio >= MIN) console.log('  PASS  ' + line);
      else fail(line + ' — want ' + MIN + ':1');
      // A big gap between declared and rendered means a layer above the copy.
      if (dm.length < 4 && declaredRatio - ratio > 0.6)
        fail(w + 'px ' + name + ' — its declared colour would give ' + declaredRatio.toFixed(2) +
             ':1 but it renders at ' + ratio.toFixed(2) + ':1, so something is painting over the text');
    }

    await ctx.close();
  }
  await b.close();
  console.log(failed ? '\n' + failed + ' FAILED' : '\nALL PASSED');
  process.exit(failed ? 1 : 0);
})();
