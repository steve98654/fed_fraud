// @ts-check
import { defineConfig } from 'astro/config';

// SITE_BASE lets the site be hosted under a subpath, e.g. GitHub Pages at
// /fed_fraud/. Defaults to the root.
export default defineConfig({
  base: process.env.SITE_BASE ?? '/',
  trailingSlash: 'ignore',
});
