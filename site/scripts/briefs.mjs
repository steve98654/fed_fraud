// Prints every agency brief (/briefs/<slug>/) to a PDF leave-behind.
//
//   npm run build && npm run briefs
//
// Serves the built site from dist/, opens each print view in Chromium
// (Playwright) and writes public/downloads/briefs/<slug>.pdf, copying each
// file into dist/ too so the current build includes it. Commit the PDFs in
// public/ so builds without a browser still ship them.
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dist = path.join(root, 'dist');
const out = path.join(root, 'public', 'downloads', 'briefs');
const distOut = path.join(dist, 'downloads', 'briefs');
const only = process.argv.slice(2);

if (!fs.existsSync(path.join(dist, 'briefs'))) {
  console.error('dist/briefs/ not found. Run "npm run build" first (without SITE_BASE).');
  process.exit(1);
}
const slugs = fs
  .readdirSync(path.join(dist, 'briefs'))
  .filter((s) => !only.length || only.includes(s))
  .sort();

const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.webp': 'image/webp', '.woff2': 'font/woff2', '.woff': 'font/woff', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(dist, p);
  if (!f.startsWith(dist) || !fs.existsSync(f)) {
    res.writeHead(404).end();
    return;
  }
  res.writeHead(200, { 'Content-Type': types[path.extname(f)] ?? 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}`;

fs.mkdirSync(out, { recursive: true });
fs.mkdirSync(distOut, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage();
const footer = (name) => `
  <div style="width:100%;font:7pt Helvetica,Arial,sans-serif;color:#586273;padding:0 0.55in;display:flex;justify-content:space-between">
    <span>The Geodesic Accountability Office · ${name} fraud brief · Draft for discussion</span>
    <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
  </div>`;

for (const slug of slugs) {
  await page.goto(`${base}/briefs/${slug}/`, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const name = (await page.title()).replace(/ fraud brief.*$/, '');
  const file = path.join(out, `${slug}.pdf`);
  await page.pdf({
    path: file,
    format: 'Letter',
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: footer(name),
  });
  fs.copyFileSync(file, path.join(distOut, `${slug}.pdf`));
  console.log(`${slug}.pdf`);
}

await browser.close();
server.close();
console.log(`${slugs.length} briefs written to public/downloads/briefs/`);
