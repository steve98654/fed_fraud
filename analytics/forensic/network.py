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
