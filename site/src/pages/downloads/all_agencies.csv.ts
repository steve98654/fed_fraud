// The all-agency register (docs/universe/data/all_agencies.csv), served as is.
import fs from 'node:fs';
import type { APIRoute } from 'astro';
import { docPath } from '../../lib/content';

export const GET: APIRoute = () =>
  new Response(fs.readFileSync(docPath('universe/data/all_agencies.csv')), {
    headers: { 'Content-Type': 'text/csv; charset=utf-8' },
  });
