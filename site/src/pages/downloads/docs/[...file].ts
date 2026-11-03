// Serves the LaTeX PDFs from ../docs (roadmap, review plan, plan and the
// one-page agency briefs) from the site itself, so downloads work on a
// private deployment without access to the GitHub repo.
import fs from 'node:fs';
import type { APIRoute } from 'astro';
import { agencies, docPath } from '../../../lib/content';

const DOC_PDFS = [
  'roadmap.pdf',
  'review_plan.pdf',
  'plan.pdf',
  'agencies/top33.pdf',
  'universe/all_agencies.pdf',
  'playbook/forensic_methods.pdf',
];

export function getStaticPaths() {
  const files = [...DOC_PDFS, ...agencies().map((a) => `agencies/${a.slug}.pdf`)];
  return files.filter((f) => fs.existsSync(docPath(f))).map((file) => ({ params: { file } }));
}

export const GET: APIRoute = ({ params }) =>
  new Response(fs.readFileSync(docPath(params.file!)), {
    headers: { 'Content-Type': 'application/pdf' },
  });
