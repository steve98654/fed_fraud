// Password gate for the whole site on Cloudflare Pages.
//
// Every request (pages, PDFs, search index) must carry HTTP Basic Auth with
// the password in the SITE_PASSWORD environment variable. Any username works
// unless SITE_USER is also set. If SITE_PASSWORD is missing the site refuses
// all requests, so a deploy can never be public by accident.
//
// Set the variables in the Pages project: Settings, Variables and Secrets, as
// type "Secret", for both Production and Preview.

const REALM = 'The Geodesic Accountability Office';

/** Constant-time string compare, so the password cannot be guessed by timing. */
async function same(a, b) {
  const enc = new TextEncoder();
  const [x, y] = await Promise.all([
    crypto.subtle.digest('SHA-256', enc.encode(a)),
    crypto.subtle.digest('SHA-256', enc.encode(b)),
  ]);
  const u = new Uint8Array(x);
  const v = new Uint8Array(y);
  let diff = 0;
  for (let i = 0; i < u.length; i++) diff |= u[i] ^ v[i];
  return diff === 0;
}

function challenge() {
  return new Response('Password required.', {
    status: 401,
    headers: {
      'WWW-Authenticate': `Basic realm="${REALM}", charset="UTF-8"`,
      'Cache-Control': 'no-store',
      'X-Robots-Tag': 'noindex, nofollow',
    },
  });
}

export async function onRequest({ request, env, next }) {
  const password = env.SITE_PASSWORD;
  if (!password) {
    return new Response('Site locked: SITE_PASSWORD is not set.', {
      status: 503,
      headers: { 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex, nofollow' },
    });
  }

  const header = request.headers.get('Authorization') ?? '';
  const [scheme, encoded] = header.split(' ');
  if (scheme !== 'Basic' || !encoded) return challenge();

  let user = '';
  let pass = '';
  try {
    const decoded = new TextDecoder().decode(Uint8Array.from(atob(encoded), (c) => c.charCodeAt(0)));
    const i = decoded.indexOf(':');
    user = decoded.slice(0, i);
    pass = decoded.slice(i + 1);
  } catch {
    return challenge();
  }

  const okPass = await same(pass, password);
  const okUser = env.SITE_USER ? await same(user, env.SITE_USER) : true;
  if (!(okPass && okUser)) return challenge();

  const res = await next();
  // Keep authenticated responses out of shared caches. Hashed build assets
  // never change, so browsers may keep them; pages are always re-checked.
  const out = new Response(res.body, res);
  const { pathname } = new URL(request.url);
  out.headers.set(
    'Cache-Control',
    pathname.startsWith('/_astro/') ? 'private, max-age=31536000, immutable' : 'private, no-cache',
  );
  return out;
}
