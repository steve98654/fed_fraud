# Ten extensions: from agency plans to a government-wide program

**Status:** Draft v0.1 (2026-11-04), for Steve's review. Builds on the
[working plan](plan.md), the [review plan](review_plan.md), the
[roadmap](roadmap.md), the [all-agency plan](universe/all_agencies.md) and
the [forensic methods handbook](playbook/forensic_methods.md).

## Bottom line

The agency plans say where fraud is likely and which public-data screens
to run first. These ten extensions supply what a leader asks next: how the
screens work across agencies, what they would return, what a first
engagement looks like, what the law allows, and whether the controls will
survive contact with people trying to beat them. Each has a planning
document; seven have tested reference code; the ROI model and live demo
also have pages on the site.

| # | Extension | Document | Code | Site |
| --- | --- | --- | --- | --- |
| 1 | Cross-agency data matching | [Cross-agency matching](playbook/cross_agency_matching.md) | `analytics/forensic/crossmatch.py` | Library |
| 2 | Network and graph analytics | [Network analytics](playbook/network_analytics.md) | `analytics/forensic/network.py` (cluster scoring) | Library |
| 3 | Recovery and ROI model | [ROI model](proposals/roi_model.md) | `analytics/roi/` | Library, ROI calculator |
| 4 | Pilot proposal kit | [Pilot kit](proposals/pilot_kit.md) | — | Library |
| 5 | Policy and legal track | [Policy and legal track](policy/legal_track.md) | — | Library |
| 6 | Procurement and contract fraud | [Procurement fraud](playbook/procurement_fraud.md) | `analytics/forensic/procurement.py` | Library |
| 7 | Grants to states | [Grants to states](research/grants_to_states.md) | `analytics/forensic/passthrough.py` | Library |
| 8 | Live demo on public data | [Live demo](demo/live_demo.md) | `analytics/demo/` | Live demo page |
| 9 | Whistleblower and tip triage | [Tip triage](playbook/tip_triage.md) | `analytics/triage/tips.py` | Library |
| 10 | Red-team playbook | [Red-team playbook](playbook/red_team.md) | — | Library |

## How they fit together

- **Engine:** cross-agency matching (1) builds the linked identities;
  network analytics (2) groups them into rings; procurement (6) and grants
  to states (7) are new screen families on top of the same spine.
- **Case for action:** the ROI model (3) gives each program a business case
  and a break-even bar; the live demo (8) shows the methods running on real
  data instead of wireframes.
- **Engagement:** the pilot kit (4) is the 90-day offer; the policy and
  legal track (5) is the map for data access; tip triage (9) is a second,
  small offer that any OIG can accept quickly.
- **Durability:** the red-team playbook (10) answers "won't they just
  adapt?" before anyone asks.

## What changed in the plan

1. **Shared screens get priority over single-agency builds for small
   programs.** The ROI model shows OPM retirement, FEMA Public Assistance
   and closed pandemic programs do not pay back on their own; they should
   ride on cross-agency matching and exclusion checks.
2. **The first Phase 2 proposal is the HHS 90-day pilot**, with SBA as the
   alternate, using the pilot kit's stop rule and metrics.
3. **Every proposal carries the ROI row, the break-even rate and the legal
   route** from the policy track.
4. **Tip triage is offered as a quick, low-data second engagement** with
   the same OIGs.

## Decisions for Steve

1. HHS-OIG or SBA OIG as the first pilot partner?
2. Publish the policy white paper on Do Not Pay data access now, or wait
   for the first pilot result?
3. Which award datasets should the live demo pull next (VA, DoD or GSA
   contracts)?
