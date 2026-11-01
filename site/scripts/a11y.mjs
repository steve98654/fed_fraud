// Accessibility check: serves the built site (dist/) and runs axe-core on
// every page against WCAG 2.1 AA. Run `npm run build` first, then
// `npm run test:a11y`. Exits non-zero on any violation.
//
// Needs a Chromium for Playwright: `npx playwright install chromium` once.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import { AxeBuilder } from '@axe-core/playwright';

const DIST = path.resolve('dist');
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.webp': 'image/webp', '.woff2': 'font/woff2', '.json': 'application/json', '.svg': 'image/svg+xml' };

if (!fs.existsSync(DIST)) {
  console.error('dist/ not found. Run `npm run build` first.');
  process.exit(2);
}

const pages = [];
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (e.name !== 'pagefind' && e.name !== '_astro') walk(p);
    } else if (e.name.endsWith('.html')) pages.push('/' + path.relative(DIST, p).replace(/index\.html$/, ''));
  }
})(DIST);

const server = http.createServer((req, res) => {
  let p = path.join(DIST, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
  if (!fs.existsSync(p)) return res.writeHead(404).end();
  res.writeHead(200, { 'content-type': TYPES[path.extname(p)] ?? 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});
await new Promise((r) => server.listen(0, r));
const origin = `http://127.0.0.1:${server.address().port}`;

const browser = await chromium.launch();
const context = await browser.newContext();
let failures = 0;
for (const p of pages.sort()) {
  const page = await context.newPage();
  await page.goto(origin + p, { waitUntil: 'load' });
  if (p === '/search/') await page.waitForSelector('#search input', { timeout: 5000 }).catch(() => {});
  const { violations } = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
  if (violations.length) {
    failures += violations.length;
    console.log(`\n✗ ${p}`);
    for (const v of violations) {
      console.log(`  [${v.impact}] ${v.id}: ${v.help} (${v.nodes.length})`);
      for (const n of v.nodes.slice(0, 3)) console.log(`      ${n.target.join(' ')}`);
    }
  }
  await page.close();
}
await browser.close();
server.close();
console.log(`\n${pages.length} pages checked, ${failures} violation type(s).`);
process.exit(failures ? 1 : 0);
