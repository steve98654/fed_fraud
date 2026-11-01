# Private hosting

The site holds draft plans that are not for the public, so it must sit behind
a login. Nothing is deployed yet. This file is the setup to follow once the
host and the list of people who get access are agreed.

## Recommendation: Cloudflare Pages behind Cloudflare Access

- **Why:** free for a small team (Access is free for up to 50 users), works with
  the static build as it is, and gates every page, file and search index
  behind an email login. Viewers get a one-time code by email; no accounts or
  passwords to manage.
- **What is in the repo:**
  - `.github/workflows/site-deploy.yml`: builds and deploys. Manual only
    (Actions tab, "Site deploy", "Run workflow").
  - `.github/workflows/site-check.yml`: builds and runs the accessibility
    check on pull requests. Deploys nothing.
  - `site/public/_headers` and `site/public/robots.txt`: `noindex` and
    security headers, so search engines stay out even if the gate is ever
    misconfigured.

### Setup (about 20 minutes, once)

1. **Create the Pages project.** In the Cloudflare dashboard: Workers & Pages,
   Create, Pages, "Direct upload", name it `geodesic-accountability-office`
   (or set the repository variable `CF_PAGES_PROJECT` to another name). Do not
   upload anything yet. From a terminal the same step is
   `npx wrangler pages project create geodesic-accountability-office --production-branch=main`.
2. **Gate it before the first deploy.** Zero Trust, Access, Applications, Add
   an application, Self-hosted:
   - Domains: `geodesic-accountability-office.pages.dev` and
     `*.geodesic-accountability-office.pages.dev` (the second covers preview
     URLs).
   - Policy: Action "Allow", Include "Emails" with each person's address (or
     "Emails ending in" `@geodesic.pro`).
   - Login method: One-time PIN.
   - Session duration: 24 hours is a reasonable default.
3. **Optional custom domain**, e.g. `gao.geodesic.pro`: Pages project, Custom
   domains. Add the same hostname to the Access application.
4. **Let GitHub deploy.** Create an API token with the "Cloudflare Pages:
   Edit" permission. In the repo's Settings, Secrets and variables, Actions,
   add secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`.
5. **Deploy and test.** Run the "Site deploy" workflow. Open the site in a
   private window and confirm you get the Cloudflare login, not the site.
   Then try an address that is not on the list and confirm it is refused.
6. **Later, if wanted:** add `push: branches: [main]` to the deploy workflow so
   every merge publishes. Only do this after step 5 passes.

## Other options considered

| Host | Access control | Notes |
| --- | --- | --- |
| Cloudflare Pages + Access | Email allowlist, one-time code | Recommended. Free at this size. |
| GitHub Pages | Private Pages need GitHub Enterprise Cloud | On other plans a Pages site is public even when the repo is private. |
| Netlify | Site password or team login on paid plans | One shared password is weaker than per-person login. |
| Vercel | Password or team-member protection on paid plans | Same trade-off as Netlify. |
| Share the build | Zip `site/dist/` and open `index.html` locally | No hosting at all; search needs a local server (`npx astro preview`). |

## Before any meeting

The "Last updated" stamps come from git history, so deploy builds must check
out full history (`fetch-depth: 0`, already set). A shallow clone would stamp
every page with the latest commit date.
