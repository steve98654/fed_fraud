# Federal fraud expansion: working plan

**Status:** Draft v0.1 (2026-10-25). Waiting on Steve's edits before step 1 starts.

## Goal

Take the SBA fraud work done with Rosemary and turn it into a repeatable
playbook. Apply it first to the agencies in the federal fraud initiative
(america.gov/fraud), then use those pilots to make the case for a
government-wide program.

## Starting assumptions (please correct)

- **Starting agencies.** We could not read america.gov/fraud directly
  because the site blocks automated access. This list comes from public
  coverage of the March 2026 anti-fraud task force executive order and DOJ's
  National Fraud Detection Center. It needs to be checked against the site.
  - Agencies named under the task force: DOJ, Treasury, HHS, Education, HUD,
    Labor, DHS, SBA and OMB, plus the Inspectors General.
  - Inspector General offices in the Detection Center: USDA, Education, HHS,
    DHS, HUD, Interior, Labor, VA, DoD (DCIS), TIGTA, SBA and SSA.
- **Data.** We start with public data: USAspending, SAM.gov, FPDS, PRAC
  data, OIG/GAO reports and DOJ press releases. Agencies would provide
  internal data only after a pilot is approved.
- **Audience.** Proposals go to agency leadership, such as deputy
  secretaries, CFOs and chief data officers, and their Inspectors General.
  They also go to the task force or OMB as the cross-agency sponsor.
- **What the SBA work produced.** Not yet in this repo. Step 1 depends on
  getting those materials.

## Plan

### Step 1: Turn the SBA work into a reusable playbook
Write down what the SBA effort does. That covers its data sources, fraud
typologies (for example identity theft, shell entities, duplicate or
stacked awards, and ineligible recipients), detection methods, outputs and
measured results. Then separate the parts that carry over to other agencies
from the parts that only fit SBA.

**Deliverable:** `docs/playbook/sba-baseline.md` and a one-page summary of
the method.

### Step 2: Profile the initiative agencies and rank them
For each agency, note its largest programs and how much money they pay out.
Also note its known fraud and improper-payment exposure, using PaymentAccuracy.gov
and OIG/GAO findings. Record which public data exists for it and how closely
it matches the SBA playbook. Rank the agencies by impact and feasibility,
and choose 2 or 3 for the first wave.

**Deliverable:** `docs/agencies/landscape.md`, with one short profile per
agency and a ranking matrix.

### Step 3: Prototype against public data for the first-wave agencies
Apply the SBA detection patterns to public data for the chosen agencies.
Build wireframes for the analyst and leadership views. The goal is a
convincing demo built from real public data, not a production system.

**Deliverable:** code under `prototypes/<agency>/` and wireframes under
`docs/wireframes/`.

### Step 4: Write proposals for agency leadership
Write one proposal per first-wave agency. Each covers the problem and
estimated dollar exposure, what the prototype found, the pilot scope and
data request, timeline, cost, success metrics and governance. Add a
cross-agency proposal that presents the shared platform as the route to
government-wide coverage.

**Deliverable:** `docs/proposals/<agency>.md` and a slide deck for each
meeting.

## Open questions for Steve

1. What does the SBA work produce today, and can it be added here?
2. Who is the first audience: a specific agency leader, an IG, OMB, or the
   task force?
3. Is any non-public data access expected for the pilots?
4. Is there a deadline or meeting the first output has to be ready for?

## Sources

- [Baker McKenzie: Trump launches nationwide antifraud task force (Mar 2026)](https://www.bakermckenzie.com/en/insight/publications/2026/03/united-states-trump-launches-nationwide-antifraud-task-force)
- [ExecutiveGov: DOJ launches National Fraud Detection Center](https://www.executivegov.com/articles/doj-national-fraud-detection-center)
