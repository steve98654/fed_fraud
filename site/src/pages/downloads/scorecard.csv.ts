// The scorecard as CSV for spreadsheets, built from the same rows as the page.
import type { APIRoute } from 'astro';
import { rows } from '../../lib/scorecard';

const cell = (v: unknown) => {
  const s = Array.isArray(v) ? v.join('; ') : String(v);
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
};

export const GET: APIRoute = () => {
  const data = rows();
  const cols = Object.keys(data[0]) as (keyof (typeof data)[0])[];
  const csv = [cols.join(','), ...data.map((r) => cols.map((c) => cell(r[c])).join(','))].join('\r\n') + '\r\n';
  return new Response(csv, { headers: { 'Content-Type': 'text/csv; charset=utf-8' } });
};
