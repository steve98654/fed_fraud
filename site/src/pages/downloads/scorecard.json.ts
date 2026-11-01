// Machine-readable scorecard, built at build time from the same rows as the
// scorecard page. Savings read "Pending" until findings are recorded.
import type { APIRoute } from 'astro';
import { rows, asOf } from '../../lib/scorecard';

export const GET: APIRoute = () =>
  new Response(
    JSON.stringify(
      {
        title: 'The Geodesic Accountability Office: federal fraud scorecard',
        as_of: asOf,
        note: 'Draft for discussion. Public data only. Savings read "Pending" until a screen passes validation and its lead package clears counsel review; only confirmed amounts count as savings. Outlays are context, not findings.',
        agencies: rows(),
      },
      null,
      2,
    ),
    { headers: { 'Content-Type': 'application/json; charset=utf-8' } },
  );
