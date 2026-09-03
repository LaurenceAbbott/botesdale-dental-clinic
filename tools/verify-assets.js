// Every LIVE local asset reference must resolve to a file on disk.
// A rename that misses a reference is silent until someone loads the page —
// which is exactly how eve-botsdale-dental.png briefly 404'd after the file
// was corrected to eve-botesdale-dental.png.
const fs = require('fs'), path = require('path');
let fail = 0;
const ok = (n, c, x = '') => { console.log(`${c ? '  PASS' : '  FAIL'}  ${n}${c ? '' : '  << ' + x}`); if (!c) fail++; };
const ROOT = '/home/user/botesdale-dental-clinic';

const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => {
  if (e.name === '.git' || e.name === 'node_modules') return [];
  const p = path.join(d, e.name);
  return e.isDirectory() ? walk(p) : (e.name.endsWith('.html') ? [p] : []);
});

const missing = [], commented = [];
for (const page of walk(ROOT)) {
  const raw = fs.readFileSync(page, 'utf8');
  // strip comments — the hero placeholders are deliberate hints, not markup
  const live = raw.replace(/<!--[\s\S]*?-->/g, '');
  const seen = new Set();
  for (const m of live.matchAll(/(?:src|href)="([^"#?]+\.(?:png|jpe?g|webp|svg|css|js|ico))(?:\?[^"]*)?"/g)) {
    const ref = m[1];
    if (/^(https?:)?\/\/|^(mailto|tel):/.test(ref)) continue;
    if (seen.has(ref)) continue;
    seen.add(ref);
    const target = path.normalize(path.join(path.dirname(page), ref));
    if (!fs.existsSync(target)) missing.push(`${path.relative(ROOT, page)} -> ${ref}`);
  }
  for (const m of raw.matchAll(/<!--[\s\S]*?-->/g)) if (/\.(png|jpe?g|webp)/.test(m[0])) commented.push(page);
}

console.log('\n== local asset references ==');
ok('every live reference resolves to a file on disk', missing.length === 0,
   JSON.stringify([...new Set(missing)].slice(0, 10), null, 1));

// the portraits specifically, since they were just renamed
console.log('\n== the team portraits ==');
const content = fs.readFileSync(path.join(ROOT, 'tools/content.py'), 'utf8');
for (const who of ['martin', 'eve']) {
  const m = content.match(new RegExp(`images/brand/(${who}[^'"]*)`));
  ok(`${who}: content.py names a file that exists`,
     m && fs.existsSync(path.join(ROOT, 'assets/images/brand', m[1])), m ? m[1] : 'not referenced');
}
const brand = fs.readdirSync(path.join(ROOT, 'assets/images/brand'));
const orphans = brand.filter(f => /\.(png|jpe?g|webp)$/.test(f) && !content.includes(f) && f !== 'favicon.svg');
ok('no orphaned portrait left behind by a rename', orphans.length === 0, JSON.stringify(orphans));

// A builder can ACCEPT an image argument and quietly drop it. c_ed did: every
// homepage block passed one, and it rendered the grey placeholder regardless,
// so dropping a real photograph into assets/ changed nothing on the page. If
// the file is on disk, the built HTML has to actually reference it.
console.log('\n== every image= that names a real file is rendered ==');
const allHtml = walk(ROOT).map(f => fs.readFileSync(f, 'utf8')).join('\n');
const unrendered = [];
for (const m of content.matchAll(/image(?:_src)?\s*=\s*'(images\/[^']+)'/g)) {
  const rel = m[1];
  if (!fs.existsSync(path.join(ROOT, 'assets', rel))) continue;   // not shot yet — fine
  if (!allHtml.includes(rel)) unrendered.push(rel);
}
ok('a photograph on disk reaches the page', unrendered.length === 0,
   JSON.stringify([...new Set(unrendered)]));

console.log(`\n(${[...new Set(commented)].length} pages carry commented-out photo placeholders — expected)`);
console.log(fail === 0 ? '\nALL PASSED' : `\n${fail} FAILED`);
process.exit(fail ? 1 : 0);
