# Network and graph analytics: scoring rings, not single payments

**Status:** Draft v0.1 (2026-11-04), for Steve's review. Extension 2 of 10
(see the [extensions overview](../extensions.md)). Reference code:
`analytics/forensic/network.py` (`communities`, `cluster_features`,
`cluster_score`, `rank_clusters`), tested on synthetic data only.

## Bottom line

Organized fraud runs through groups of entities that look ordinary one at a
time: twenty hospices that each bill a plausible amount, eight PPP
borrowers with plausible payrolls, five "small businesses" that each win
a few set-asides. What gives them away is what they share: an address, an
officer, a phone line, a bank account, a preparer. The forensic methods
handbook already builds the shared-attribute graph and propagates risk
from known bad actors. This extension adds the step that turns a graph
into a work queue: **split the graph into communities, describe each
community with a few features, and rank communities by a calibrated
score**, so investigators open the ring, not one member of it.

## 1. Graph

Nodes are entities (businesses, providers, borrowers). An edge joins two
entities that share an attribute: address, officer or owner, phone, email,
bank account, registered agent, or IP or device in Phase 2. Edge weight
follows the handbook (section 8): each shared attribute adds
1 / log(1 + degree), so a phone shared by two firms counts far more than a
registered-agent address shared by 4,000. Attributes on the benign-hub
list (registered agents, mail centers, hospitals, large payroll firms) and
attributes with more than 25 entities are dropped.

## 2. From components to communities

Connected components chain together through single weak links, so one
shared accountant can glue two unrelated rings into one blob. Weighted
label propagation splits a component into groups that are densely tied
inside and loosely tied outside. It is deterministic for a given seed,
needs no tuning and runs in near-linear time, which matters at SAM.gov
scale (several hundred thousand active
registrations). Louvain or Leiden are
drop-in alternatives in a graph database.

## 3. Cluster features

| Feature | Definition | Why it matters |
| --- | --- | --- |
| Size | Entities in the community | Rings are usually 3 to 50 entities |
| Density | Internal edges / possible edges | Rings are tightly interconnected; franchises are star-shaped |
| Bank share | Share of members sharing a bank account with another member | The strongest single sign of common control |
| New share | Share first seen in the last two years | Rings form fast around a new program or rule change |
| Dollars | Total paid to the community | Sets priority among similar scores |
| Seed risk | Highest risk-propagation score from excluded, debarred or charged entities | Known bad actors nearby |

## 4. Score

A logistic score combines the features, with size and dollars on log
scales so a 200-outlet franchise does not outrank a six-firm ring that
shares bank accounts. The default weights in `CLUSTER_WEIGHTS` are starting
values. Before any cluster is referred they are refit on confirmed rings
(DOJ case releases, OIG reports, the SBA case set) using the likelihood
ratio method in the handbook section 12, and the score must meet the
review plan's release bar: known rings at least five times more common in
the top 5% than in the population.

## 5. What an investigator sees

For each ranked cluster the tool shows: members and their awards or
payments; the shared attributes that tie them, strongest first; a small
graph drawing; dates of formation; any seed (excluded or charged entity)
within two hops; and the reason codes behind the score. The tool preview
pages on the site follow this layout.

## 6. Where it applies first

| Roadmap idea | Graph | Seeds |
| --- | --- | --- |
| HHS-1, HHS-2 hospice and home health | Owners, managing employees, addresses from CMS enrollment files | LEIE, revoked providers, DOJ defendants |
| SBA-1, SBA-3 loan rings | Borrower addresses, lenders, agents, NAICS | Charged PPP and EIDL defendants |
| DOD-1, VA-1 set-aside fronts | SAM.gov officers, addresses, parent firms | SAM exclusions, SBA protests sustained |
| TREAS-2 ERC and EITC promoters | Preparers and promoters in charged cases | DOJ Tax Division cases |
| X-4 hidden common control | All of the above, linked through cross-agency matching | All exclusion lists |

## 7. Limits

- Public data shows registrations, not control. A shared officer may be a
  part-time bookkeeper; the score asks a question, it does not answer one.
- Rings adapt by spreading attributes thin (one phone per firm). The
  [red-team playbook](red_team.md) sets out how the features respond.
- Bank accounts are the strongest feature and are not public; until Phase 2
  the bank-share feature is zero and the score leans on officers, phones
  and addresses.

## 8. Next steps

1. Fit weights on the SBA confirmed set (weeks 5 to 6).
2. Run on HHS hospice enrollment data alongside HHS-1 (weeks 6 to 8).
3. Add a cluster view to the HHS-1 tool preview.
