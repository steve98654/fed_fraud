"""Tests for the extension modules (cross-agency matching, cluster scoring,
procurement, grants to states, ROI model, tip triage) on synthetic data
only. No real entity, payee or tip appears here.

Run from the repo root:  python3 -m unittest discover -s analytics/tests -t analytics
"""
import json
import random
import unittest
from datetime import date
from types import SimpleNamespace

import numpy as np

from forensic import crossmatch, network, passthrough, procurement
from forensic.linkage import FSModel
from roi import model as roi
from triage import tips

KEY = b"test-key-not-a-secret"


def fs_model():
    # name, address, dob, tin, bank, phone, email
    return FSModel(crossmatch.FIELDS, m=[0.95, 0.8, 0.9, 0.98, 0.9, 0.7, 0.7], u=[0.01, 0.01, 0.005, 0.0001, 0.001, 0.005, 0.001], p=0.05)


class TestCrossmatch(unittest.TestCase):
    def setUp(self):
        tin = crossmatch.keyed_hash("12-3456789", KEY)
        bank = crossmatch.keyed_hash("021000021-99887766", KEY)
        R = crossmatch.ProgramRecord
        self.recs = [
            R("sba1", "SBA-PPP", "Acme Holdings, L.L.C.", "12 North Main Street 20001", "2019", tin, bank, paid=[(date(2021, 3, 1), 150000)]),
            R("cms1", "CMS-PECOS", "ACME HOLDINGS LLC", "12 N Main St 20001", "2019", tin, "", paid=[(date(2023, 6, 1), 80000)]),
            R("usda1", "USDA-FSA", "Acme Holdings", "12 n main st 20001", "", tin, bank, paid=[(date(2022, 1, 5), 40000)]),
            R("ui1", "STATE-UI", "Acme Holdings", "12 North Main Street 20001", "2019", tin, "", paid=[(date(2021, 4, 1), 9000)]),
            R("x1", "SBA-PPP", "Zenith Farms", "9 Elm Rd 30301", "1990", crossmatch.keyed_hash("98-7654321", KEY), "", paid=[(date(2021, 3, 1), 20000)]),
        ]
        self.by_id = {r.record_id: r for r in self.recs}
        self.clusters = crossmatch.link(self.recs, fs_model(), threshold=8.0)

    def test_normalization(self):
        self.assertEqual(crossmatch.normalize_name("Acme Holdings, L.L.C."), "acme holdings")
        self.assertEqual(crossmatch.normalize_address("12 North Main Street"), "12 n main st")
        self.assertEqual(crossmatch.keyed_hash("12-3456789", KEY), crossmatch.keyed_hash("123456789", KEY))
        self.assertNotEqual(crossmatch.keyed_hash("123456789", KEY), crossmatch.keyed_hash("123456789", b"other"))

    def test_links_one_identity_across_programs(self):
        self.assertEqual(self.clusters[0], {"sba1", "cms1", "usda1", "ui1"})
        self.assertIn({"x1"}, self.clusters)

    def test_stacking_and_exclusive(self):
        flags = crossmatch.program_stacking(self.clusters, self.by_id, max_programs=3, exclusive=[{"SBA-PPP", "STATE-UI"}])
        checks = sorted(f.check for f in flags)
        self.assertEqual(checks, ["exclusive", "stacking"])
        self.assertEqual(flags[0].amount, 279000)

    def test_paid_after_death_reaches_other_programs(self):
        # death recorded only against the CMS record; the SBA and USDA payments are later
        flags = crossmatch.paid_after_event(self.clusters, self.by_id, {"cms1": date(2021, 1, 1)}, "after-death", grace_days=30)
        self.assertEqual(len(flags), 1)
        self.assertEqual(flags[0].amount, 150000 + 80000 + 40000 + 9000)

    def test_shared_bank_across_unrelated(self):
        R = crossmatch.ProgramRecord
        bank = crossmatch.keyed_hash("acct-1", KEY)
        recs = [R(f"p{i}", "STATE-UI", n, f"{i} Oak Ave 1000{i}", "", crossmatch.keyed_hash(f"tin{i}", KEY), bank, paid=[(date(2021, 1, 1), 1000)])
                for i, n in enumerate(["Ann Lee", "Bo Diaz", "Cy Park", "Di Moss"])]
        by_id = {r.record_id: r for r in recs}
        clusters = crossmatch.link(recs, fs_model(), threshold=8.0)
        self.assertEqual(len(clusters), 4)  # a bank account alone is not enough to merge identities
        flags = crossmatch.shared_identifier_conflicts(clusters, by_id, "bank_hash", min_identities=3)
        self.assertEqual(len(flags), 1)
        self.assertEqual(flags[0].amount, 4000)


class TestClusters(unittest.TestCase):
    def test_ring_outranks_franchise(self):
        rng = random.Random(3)
        attrs, dollars, first = {}, {}, {}
        # A 6-firm ring: shared bank accounts, phones and one address, all new.
        for i in range(6):
            e = f"ring{i}"
            attrs[e] = {"bank:B1" if i < 3 else "bank:B2", "phone:P1", "addr:A1", f"officer:O{i % 2}"}
            dollars[e] = 400_000
            first[e] = 2025
        # A 30-outlet franchise: one shared brand officer, distinct banks, old.
        for i in range(30):
            e = f"fr{i}"
            attrs[e] = {f"bank:F{i}", f"addr:FA{i}", "officer:BRAND", f"phone:FP{rng.randrange(10)}"}
            dollars[e] = 900_000
            first[e] = 2005
        ranked = network.rank_clusters(attrs, dollars, first, as_of_year=2026, max_degree=40)
        self.assertTrue(ranked[0][1] <= {f"ring{i}" for i in range(6)})
        self.assertGreater(ranked[0][0], ranked[-1][0])

    def test_communities_split_bridged_groups(self):
        edges = {}
        for g in ("a", "b"):
            for i in range(5):
                for j in range(i + 1, 5):
                    edges[(f"{g}{i}", f"{g}{j}")] = 1.0
        edges[("a0", "b0")] = 0.2  # weak bridge
        comms = network.communities(edges)
        self.assertEqual(sorted(len(c) for c in comms), [5, 5])


class TestProcurement(unittest.TestCase):
    def test_growth_outlier_and_single_offer(self):
        rng = random.Random(5)
        A = procurement.Award
        awards = [A(f"c{i}", f"v{i % 7}", "OFF1", "541512", 1e6, 1e6 * rng.uniform(1.0, 1.3), offers=rng.choice([2, 3, 4, 1]), competed=True)
                  for i in range(40)]
        awards.append(A("big", "v9", "OFF1", "541512", 1e6, 6.5e6, offers=1))
        out = procurement.modification_outliers(awards)
        self.assertEqual(out[0][0], "big")
        rates = procurement.single_offer_rates(awards)
        self.assertIn("OFF1", rates)
        self.assertGreater(procurement.incumbent_lock(awards)[("OFF1", "541512")], 0)

    def test_mods_below_threshold(self):
        a = procurement.Award("c", "v", "o", "n", 1e6, 2e6, mods=[240_000, 245_000, 100_000, 249_000])
        self.assertEqual(procurement.mods_below_threshold(a, 250_000), 3)

    def test_set_aside_checks(self):
        c = procurement.set_aside_checks("v", 60e6, None, 34e6, None, 10e6, 7e6, "services", linked_large_firms=1)
        self.assertEqual(len(c.reasons), 3)
        ok = procurement.set_aside_checks("v", 5e6, 20, 34e6, 500, 10e6, 3e6, "services")
        self.assertEqual(ok.reasons, [])

    def test_set_aside_share_jump(self):
        self.assertEqual(procurement.set_aside_share_jump({2022: (0.1e6, 1e6), 2023: (2.5e6, 3e6)}), [2023])


class TestPassthrough(unittest.TestCase):
    def test_state_outliers(self):
        rng = random.Random(9)
        rows = [passthrough.StateMetric(f"S{i}", rng.gauss(100, 10), 10_000) for i in range(30)]
        rows.append(passthrough.StateMetric("HOT", 400, 10_000))
        flagged = [s for s, *_ in passthrough.state_outliers(rows)]
        self.assertEqual(flagged[0], "HOT")

    def test_repeat_findings_and_concentration(self):
        F = passthrough.AuditFinding
        fs = [F("U1", y, "10.555", True, 1e5, y > 2021) for y in (2021, 2022, 2023)] + [F("U2", 2023, "10.555", True, 0, False)]
        self.assertEqual(list(passthrough.repeat_finding_entities(fs)), ["U1"])
        conc = passthrough.subaward_concentration([("ST", "A", 90.0), ("ST", "B", 5.0), ("ST", "C", 5.0)])
        self.assertEqual(conc["ST"][1], "A")
        self.assertAlmostEqual(conc["ST"][2], 0.9)

    def test_growth_without_caseload(self):
        self.assertEqual(passthrough.growth_without_caseload({2022: 10, 2023: 25, 2024: 26}, {2022: 100, 2023: 110, 2024: 112}), [2023])


class TestROI(unittest.TestCase):
    def setUp(self):
        self.p = roi.Program("X", "Test program", 1e9, "open", "X-1", "synthetic", 0.5)

    def test_likely_scenario_by_hand(self):
        r = roi.simulate(self.p, roi.likely())
        # year-3 steady state benefit, undiscounted
        a = {k: v[1] for k, v in roi.ASSUMPTIONS.items()}
        caught = 1e9 * 0.5 * a["detectable"] * a["new_detection"]
        benefit = caught * (a["prevent"] + (1 - a["prevent"]) * a["recovery"]) * (1 + a["deterrence"])
        pv = sum(benefit * ramp * (1 + roi.DISCOUNT) ** -(t + 0.5) for t, ramp in enumerate(roi.RAMP))
        self.assertAlmostEqual(r["pv_benefit"][0], pv, delta=1)

    def test_closed_program_only_recovers(self):
        closed = roi.Program("X", "Closed", 1e9, "closed", "X-1", "synthetic", 1.0)
        a = roi.likely()
        a["recovery"] = np.array([0.0])
        self.assertEqual(roi.simulate(closed, a)["pv_benefit"][0], 0.0)

    def test_monte_carlo_ordering_and_breakeven(self):
        s = roi.summarize(self.p, n=4000)
        self.assertLess(s["net"][10], s["net"][50])
        self.assertLess(s["net"][50], s["net"][90])
        b = roi.breakeven_new_detection(self.p)
        a = roi.likely()
        a["new_detection"] = np.array([b * 1.01])
        self.assertGreater(roi.simulate(self.p, a)["net"][0], 0)

    def test_program_file_loads(self):
        progs = roi.load_programs()
        self.assertGreaterEqual(len(progs), 10)
        self.assertTrue(all(0 < p.reach <= 1 for p in progs))


class TestTips(unittest.TestCase):
    GOOD = ("I worked as a billing clerk at Sunrise Hospice from March 2024 to June 2025. My boss told us to bill "
            "Medicare for patients we never saw, about $40,000 a month. I kept copies of the invoices and emails.")
    VAGUE = "The government is corrupt, wake up people."
    URGENT = "The owner is shredding records tonight before the audit of our Medicaid billing."

    def test_rule_ranks_specific_tip_first(self):
        q = tips.triage_queue({"vague": self.VAGUE, "good": self.GOOD})
        self.assertEqual(q[0][0], "good")
        good = dict(q)["good"]
        self.assertEqual(good.program, "Medicare")
        self.assertEqual(good.scheme, "Billing for services not provided")
        self.assertTrue(good.whistleblower_protection)

    def test_urgent_goes_first(self):
        q = tips.triage_queue({"good": self.GOOD, "urgent": self.URGENT})
        self.assertEqual(q[0][0], "urgent")

    def test_twelve_letter_word_is_not_an_identifier(self):
        self.assertNotIn("gives an identifier", tips.rule_score("construction work was billed twice to the agency by the firm").reasons)

    def test_evaluate(self):
        q = tips.triage_queue({"a": self.GOOD, "b": self.VAGUE, "c": "hello", "d": "nothing much", "e": "ok"})
        m = tips.evaluate(q, {"a"}, top_share=0.2)
        self.assertEqual(m["recall_at_k"], 1.0)
        self.assertEqual(m["lift"], 5.0)

    @unittest.skipUnless(__import__("importlib").util.find_spec("anthropic"), "anthropic SDK not installed")
    def test_claude_score_with_fake_client(self):
        payload = {"actionability": 90, "urgent": False, "program": "Medicare", "scheme": "Billing for services not provided",
                   "summary": "A former clerk reports billing for patients not seen.", "reasons": ["insider", "amounts"],
                   "entities": ["Sunrise Hospice"], "whistleblower_protection": True}
        calls = {}

        def create(**kw):
            calls.update(kw)
            return SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text=json.dumps(payload))])

        fake = SimpleNamespace(beta=SimpleNamespace(messages=SimpleNamespace(create=create)))
        t = tips.claude_score(self.GOOD, client=fake)
        self.assertEqual(t.scorer, "claude+rules")
        self.assertEqual(t.entities, ["Sunrise Hospice"])
        self.assertEqual(calls["model"], "claude-opus-5-5")
        self.assertIn("<tip>", calls["messages"][0]["content"])

        def refuse(**kw):
            return SimpleNamespace(stop_reason="refusal", content=[])

        fake.beta.messages.create = refuse
        self.assertEqual(tips.claude_score(self.GOOD, client=fake).scorer, "rules")


if __name__ == "__main__":
    unittest.main()
