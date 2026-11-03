# Hosting on Cloudflare Pages, with a password

The site holds draft plans that are not for the public. On Cloudflare Pages
it sits behind a password: `site/functions/_middleware.js` asks every visitor
for it before serving any page, PDF or search file. If no password is set, the
site shows "Site locked" to everyone, so a deploy can never be public by
accident.

Viewers see their browser's login box. Any username works; the password is the
one you set. Send the password separately from the link.

## Set it up (about 15 minutes, once)

You need a free Cloudflare account and the Cloudflare GitHub app allowed on
`steve98654/fed_fraud` (Cloudflare asks for this in step 2).

1. **Start a Pages project.** In the Cloudflare dashboard go to
   **Compute (Workers) → Workers & Pages → Create application**, choose the
   **Pages** tab, then **Import an existing Git repository**. (Older dashboards
   call this **Connect to Git**.)
2. **Pick the repo.** Connect GitHub if asked, give the Cloudflare app access
   to `steve98654/fed_fraud`, select it and click **Begin setup**.
3. **Build settings.** Enter exactly:

   | Setting | Value |
   | --- | --- |
   | Project name | `geodesic-accountability-office` (becomes `geodesic-accountability-office.pages.dev`) |
   | Production branch | `main` |
   | Framework preset | `Astro` |
   | Build command | `npm run build` |
   | Build output directory | `dist` |
   | Root directory (under *Advanced*) | `site` |

4. **Password, before the first build.** Still on that page, open
   **Environment variables (advanced)** and add:

   | Variable | Value | Type |
   | --- | --- | --- |
   | `SITE_PASSWORD` | the password you will share | Encrypt / Secret |
   | `NODE_VERSION` | `22` | Plain text |

   Optional: `SITE_USER` if you also want a fixed username.
5. Click **Save and Deploy**. The first build takes two to three minutes.
6. **Make sure the password also covers preview links.** Open the project,
   **Settings → Variables and Secrets**, and check that `SITE_PASSWORD` exists
   for both **Production** and **Preview**. Add it to Preview if it is missing.
   (Even without it, previews show "Site locked", not the content.)
7. **Test it.** Open `https://geodesic-accountability-office.pages.dev` in a
   private window. You should get a login box. A wrong password must be
   refused, and the right one must show the scorecard.

From then on, every merge to `main` redeploys the site automatically.

### Changing the password

Edit `SITE_PASSWORD` under **Settings → Variables and Secrets**, then open
**Deployments**, pick the latest one and choose **Retry deployment**. A new
value only applies to deployments made after the change.

### Optional extras

- **Your own address**, for example `gao.geodesic.pro`: project →
  **Custom domains → Set up a custom domain**. The password covers it too.
- **Fewer preview URLs**: **Settings → Builds → Branch control**, set
  preview deployments to **None** so only `main` is published.

## Stronger option: per-person logins with Cloudflare Access

A shared password can be forwarded. If you later need to know who viewed the
site, or to remove one person, put Cloudflare Access in front instead of (or as
well as) the password. It is free for up to 50 users:

1. **Zero Trust → Access → Applications → Add an application → Self-hosted.**
2. Domains: `geodesic-accountability-office.pages.dev` and
   `*.geodesic-accountability-office.pages.dev`, plus any custom domain.
3. Policy: Action **Allow**, Include **Emails**, with each person's address.
4. Login method: **One-time PIN**. Viewers get a code by email.

To drop the password once Access is on, delete `SITE_PASSWORD` and the
`site/functions/` folder in the same change, since without the variable the
gate locks the site.

## What is in the repo

- `site/functions/_middleware.js`: the password gate.
- `site/.nvmrc`: Node 22 for the Cloudflare builder.
- `site/public/_headers`, `site/public/robots.txt`: `noindex` and security
  headers, so search engines stay out.
- `.github/workflows/site-deploy.yml`: an optional manual deploy from GitHub
  Actions (needs `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` secrets).
  Not needed with the dashboard setup above.
- `.github/workflows/site-check.yml`: build and accessibility check on pull
  requests.

## Notes

- The "Last updated" dates come from git history. If the builder clones only
  the latest commit, the build fetches the rest of the history itself.
- Cloudflare's free plan allows 100,000 password-checked requests a day. A page
  view is about 20 requests, so that is roughly 5,000 page views a day.
- To try the gate locally: `npm run build`, put `SITE_PASSWORD="test"` in
  `site/.dev.vars`, and run `npx wrangler pages dev dist`.
