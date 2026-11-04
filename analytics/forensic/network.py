"""Entity networks: shared-attribute graphs, components, hub discounting and
risk propagation from known bad actors.

Pure Python so it runs without graph libraries; for the full spine use the
same logic in a graph database or networkx. See
docs/playbook/forensic_methods.md section 8.
"""
from __future__ import annotations

import math
from collections import defaultdict
from itertools import combinations


class UnionFind:
    def __init__(self):
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def shared_attribute_edges(attrs: dict[str, set[str]], max_degree: int = 25, benign: set[str] | None = None) -> dict[tuple[str, str], float]:
    """Project an entity-attribute bipartite graph (attributes are addresses,
    phones, officers, emails, bank accounts) onto entities.

    Edge weight between two entities = sum over shared attributes of
    1 / log(1 + degree(attribute)), an Adamic-Adar style discount, so a
    phone shared by two firms counts far more than a registered-agent
    address shared by 4,000. Attributes on the benign-hub list, or with more
    than `max_degree` entities, are dropped."""
    benign = benign or set()
    by_attr: dict[str, list[str]] = defaultdict(list)
    for ent, a in attrs.items():
        for x in a:
            by_attr[x].append(ent)
    edges: dict[tuple[str, str], float] = defaultdict(float)
    for x, ents in by_attr.items():
        deg = len(ents)
        if deg < 2 or deg > max_degree or x in benign:
            continue
        w = 1.0 / math.log(1 + deg)
        for a, b in combinations(sorted(ents), 2):
            edges[(a, b)] += w
    return dict(edges)


def components(edges: dict[tuple[str, str], float], min_weight: float = 0.0) -> list[set[str]]:
    """Connected components using edges at or above `min_weight`, largest first."""
    uf = UnionFind()
    for (a, b), w in edges.items():
        if w >= min_weight:
            uf.union(a, b)
    groups: dict[str, set[str]] = defaultdict(set)
    for x in list(uf.parent):
        groups[uf.find(x)].add(x)
    return sorted(groups.values(), key=len, reverse=True)


def personalized_pagerank(edges: dict[tuple[str, str], float], seeds: set[str], alpha: float = 0.15, iters: int = 100) -> dict[str, float]:
    """Risk propagation: random walk with restart to the seed set (excluded,
    debarred or convicted entities). Scores measure closeness to known bad
    actors through weighted shared attributes. alpha is the restart
    probability; higher alpha keeps risk closer to the seeds."""
    nbrs: dict[str, dict[str, float]] = defaultdict(dict)
    for (a, b), w in edges.items():
        nbrs[a][b] = nbrs[a].get(b, 0) + w
        nbrs[b][a] = nbrs[b].get(a, 0) + w
    nodes = set(nbrs) | seeds
    restart = {n: (1 / len(seeds) if n in seeds else 0.0) for n in nodes}
    r = dict(restart)
    for _ in range(iters):
        nxt = {n: alpha * restart[n] for n in nodes}
        for n in nodes:
            out = nbrs.get(n)
            if not out:
                # dangling mass returns to seeds
                for s in seeds:
                    nxt[s] += (1 - alpha) * r[n] / len(seeds)
                continue
            tot = sum(out.values())
            for m, w in out.items():
                nxt[m] += (1 - alpha) * r[n] * w / tot
        r = nxt
    return r


def colocation_excess(observed_entities: int, address_capacity_expected: float) -> float:
    """Poisson upper-tail probability of seeing at least `observed_entities`
    registered at one address when the address type (single-family home,
    small office, mailbox store) would predict `address_capacity_expected`.
    Small values flag addresses with more entities than their type explains."""
    lam = address_capacity_expected
    k = observed_entities
    # P(X >= k) = 1 - sum_{i<k} e^-lam lam^i / i!
    term = math.exp(-lam)
    cdf = 0.0
    for i in range(k):
        cdf += term
        term *= lam / (i + 1)
    return max(0.0, 1.0 - cdf)


# ---------------------------------------------------------------------------
# Cluster scoring: rank rings, not single payments.
# See docs/playbook/network_analytics.md.
# ---------------------------------------------------------------------------
def communities(edges: dict[tuple[str, str], float], iters: int = 20, seed: int = 0) -> list[set[str]]:
    """Weighted label propagation (Raghavan, Albert and Kumara 2007). Splits a
    large connected component into tightly knit groups, so one shared
    registered agent does not glue two unrelated rings together. Ties break
    on the smallest label, so results are deterministic for a given seed."""
    import random

    nbrs: dict[str, dict[str, float]] = defaultdict(dict)
    for (a, b), w in edges.items():
        nbrs[a][b] = nbrs[a].get(b, 0) + w
        nbrs[b][a] = nbrs[b].get(a, 0) + w
    label = {n: n for n in nbrs}
    order = sorted(nbrs)
    rng = random.Random(seed)
    for _ in range(iters):
        rng.shuffle(order)
        changed = False
        for n in order:
            score: dict[str, float] = defaultdict(float)
            for m, w in nbrs[n].items():
                score[label[m]] += w
            best = max(score.values())
            new = min(lab for lab, s in score.items() if s == best)
            if new != label[n]:
                label[n] = new
                changed = True
        if not changed:
            break
    groups: dict[str, set[str]] = defaultdict(set)
    for n, lab in label.items():
        groups[lab].add(n)
    return sorted(groups.values(), key=len, reverse=True)


def cluster_features(cluster: set[str], edges: dict[tuple[str, str], float], attrs: dict[str, set[str]],
                     dollars: dict[str, float], first_seen_year: dict[str, int], as_of_year: int,
                     risk: dict[str, float] | None = None) -> dict[str, float]:
    """Features of one cluster of entities. Attribute ids are expected to be
    typed ("bank:...", "phone:...", "addr:...", "officer:...").

    size              number of entities
    density           internal edges / possible edges
    bank_share        share of entities that share a bank account with another member
    new_share         share of entities first seen in the last two years
    dollars           total paid to the cluster
    dollar_per_entity dollars / size
    seed_risk         max personalized PageRank score in the cluster (0 if none)
    """
    n = len(cluster)
    internal = [w for (a, b), w in edges.items() if a in cluster and b in cluster]
    density = len(internal) / (n * (n - 1) / 2) if n > 1 else 0.0
    banks: dict[str, int] = defaultdict(int)
    for e in cluster:
        for x in attrs.get(e, ()):
            if x.startswith("bank:"):
                banks[x] += 1
    shared_bank_ents = {e for e in cluster if any(banks[x] > 1 for x in attrs.get(e, ()) if x.startswith("bank:"))}
    total = sum(dollars.get(e, 0.0) for e in cluster)
    return {
        "size": float(n),
        "density": density,
        "bank_share": len(shared_bank_ents) / n if n else 0.0,
        "new_share": sum(1 for e in cluster if as_of_year - first_seen_year.get(e, 0) <= 2) / n if n else 0.0,
        "dollars": total,
        "dollar_per_entity": total / n if n else 0.0,
        "seed_risk": max((risk or {}).get(e, 0.0) for e in cluster),
    }


# Default weights: log-odds points per unit of each feature. Starting values
# only; calibrate against confirmed rings (scoring.likelihood_ratio) before
# any cluster is referred.
CLUSTER_WEIGHTS = {"density": 1.5, "bank_share": 2.5, "new_share": 1.5, "seed_risk": 20.0, "log_size": 0.8, "log_dollars": 0.3}


def cluster_score(f: dict[str, float], weights: dict[str, float] | None = None) -> float:
    """Logistic risk score in (0, 1) for one cluster. Size and dollars enter
    on a log scale so a 200-entity franchise network does not outrank a
    tight 6-entity ring that shares bank accounts."""
    w = weights or CLUSTER_WEIGHTS
    z = -6.0
    z += w["density"] * f["density"] + w["bank_share"] * f["bank_share"] + w["new_share"] * f["new_share"]
    z += w["seed_risk"] * f["seed_risk"]
    z += w["log_size"] * math.log(max(f["size"], 1.0))
    z += w["log_dollars"] * math.log10(max(f["dollars"], 1.0))
    return 1 / (1 + math.exp(-z))


def rank_clusters(attrs: dict[str, set[str]], dollars: dict[str, float], first_seen_year: dict[str, int],
                  as_of_year: int, seeds: set[str] | None = None, min_size: int = 3,
                  max_degree: int = 25, benign: set[str] | None = None) -> list[tuple[float, set[str], dict[str, float]]]:
    """End to end: shared-attribute graph, communities, features, score.
    Returns (score, members, features) for clusters of at least `min_size`,
    highest score first."""
    edges = shared_attribute_edges(attrs, max_degree=max_degree, benign=benign)
    risk = personalized_pagerank(edges, seeds) if seeds else {}
    out = []
    for c in communities(edges):
        if len(c) < min_size:
            continue
        f = cluster_features(c, edges, attrs, dollars, first_seen_year, as_of_year, risk)
        out.append((cluster_score(f), c, f))
    return sorted(out, key=lambda t: t[0], reverse=True)
