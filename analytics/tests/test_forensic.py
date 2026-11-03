"""Tests for analytics/forensic on synthetic data only (no real entities).

Run from the repo root:  python3 -m unittest discover -s analytics/tests -t analytics
"""
import math
import random
import unittest
from datetime import date, timedelta

import numpy as np

from forensic import bids, digits, duplicates, linkage, network, outliers, sampling, scoring, stats


class TestStats(unittest.TestCase):
    def test_chi2_sf_matches_tables(self):
        self.assertAlmostEqual(stats.chi2_sf(3.841459, 1), 0.05, places=5)
        self.assertAlmostEqual(stats.chi2_sf(15.507313, 8), 0.05, places=5)
        self.assertAlmostEqual(stats.chi2_sf(112.022, 89), 0.05, places=3)

    def test_benjamini_hochberg(self):
        p = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074, 0.205, 0.212, 0.216]
        self.assertEqual(sum(stats.benjamini_hochberg(p, 0.05)), 2)


class TestDigits(unittest.TestCase):
    def setUp(self):
        rng = random.Random(1)
        # Log-uniform over five orders of magnitude follows Benford's law.
        self.clean = [10 ** rng.uniform(1, 6) for _ in range(20000)]
        # Invented amounts: people pick "middle" leading digits too often.
        self.made_up = [rng.uniform(3000, 7999) for _ in range(20000)]

    def test_expected_sums_to_one(self):
        for t in ("first", "second", "first_two", "last_two"):
            self.assertAlmostEqual(sum(digits.benford_expected(t).values()), 1.0, places=12)
        self.assertAlmostEqual(digits.benford_expected("first")[1], 0.30103, places=5)

    def test_clean_data_conforms(self):
        r = digits.digit_test(self.clean, "first")
        self.assertEqual(r.conformity, "close")
        self.assertGreater(r.p_value, 0.001)
        r2 = digits.digit_test(self.clean, "first_two")
        self.assertIn(r2.conformity, ("close", "acceptable"))

    def test_made_up_data_fails(self):
        r = digits.digit_test(self.made_up, "first")
        self.assertEqual(r.conformity, "nonconformity")
        self.assertLess(r.p_value, 1e-10)
        self.assertTrue(set(r.spikes()) <= {3, 4, 5, 6, 7})

    def test_round_numbers_and_duplicates(self):
        vals = [1000.0] * 30 + [1234.56] * 5 + [float(i) + 0.37 for i in range(100, 400)]
        self.assertAlmostEqual(digits.round_number_share(vals, 1000), 30 / 335)
        share, p = digits.round_number_test(vals, 1000, 0.01)
        self.assertLess(p, 1e-6)
        self.assertEqual(digits.number_duplication(vals, 1)[0], (1000.0, 30))

    def test_last_two_and_rsf(self):
        r = digits.digit_test([i + 0.99 for i in range(100, 2100)], "last_two")
        self.assertLess(r.p_value, 1e-10)  # every amount ends in .99
        rsf = digits.relative_size_factor({"v1": [100, 110, 5000], "v2": [100, 120]})
        self.assertAlmostEqual(rsf["v1"], 5000 / 110)


class TestDuplicates(unittest.TestCase):
    def test_invoice_normalization(self):
        self.assertEqual(duplicates.normalize_invoice("INV-00O123"), duplicates.normalize_invoice("123"))
        self.assertEqual(duplicates.damerau_levenshtein("12345", "12354"), 1)

    def test_duplicate_tiers(self):
        d = date(2026, 3, 1)
        P = duplicates.Payment
        pays = [
            P("1", "ACME", 500.0, d, "A100"),
            P("2", "ACME", 500.0, d, "A100"),  # exact
            P("3", "ACME", 500.0, d + timedelta(30), "a-100"),  # same invoice, normalized
            P("4", "ACME", 500.0, d + timedelta(10), "A1001"),  # near-identical
            P("5", "ACME CORP", 500.0, d, "A100"),  # different vendor
            P("6", "ACME", 499.0, d, "A100"),
        ]
        rules = {(x.a, x.b): x.rule for x in duplicates.duplicate_pairs(pays)}
        self.assertIn("date", rules[("1", "2")])
        self.assertIn("different date", rules[("1", "3")])
        self.assertIn("near-identical", rules[("1", "4")])
        self.assertIn("different vendor", rules[("1", "5")])
        self.assertFalse(any("6" in k for k in rules))

    def test_split_purchases(self):
        d = date(2026, 5, 4)
        P = duplicates.Payment
        pays = [P(str(i), "SUPPLY", 9000.0, d + timedelta(i), payer="card7") for i in range(2)]
        pays.append(P("x", "SUPPLY", 9000.0, d + timedelta(20), payer="card7"))
        flags = duplicates.split_purchases(pays, threshold=15000, window_days=3)
        self.assertEqual(len(flags), 1)
        self.assertEqual(flags[0].ids, ("0", "1"))

    def test_impossible_days_and_death(self):
        d = date(2026, 1, 5)
        E = duplicates.TimeEntry
        es = [E("atty1", d, 10, "m1"), E("atty1", d, 9, "m2"), E("atty1", d, 7.5, "m3"), E("atty2", d, 8, "m1")]
        self.assertEqual(duplicates.impossible_days(es), {("atty1", d): 26.5})
        late = duplicates.services_after_death({"p1": [d, d + timedelta(40)]}, {"p1": d + timedelta(1)})
        self.assertEqual(late, {"p1": [d + timedelta(40)]})


class TestOutliers(unittest.TestCase):
    def test_robust_z_resists_outliers(self):
        z = outliers.robust_z([10, 11, 9, 10, 12, 10, 500])
        self.assertGreater(z[-1], 100)
        self.assertLess(abs(z[0]), 1)

    def test_empirical_bayes_shrinks_small_counts(self):
        rng = np.random.default_rng(3)
        E = rng.uniform(5, 200, 400)
        theta = rng.gamma(20, 1 / 20, 400)
        y = rng.poisson(theta * E)
        prior = outliers.fit_gamma_prior(list(y), list(E))
        self.assertAlmostEqual(prior.alpha / prior.beta, 1.0, delta=0.1)
        small, _ = outliers.shrunk_rate_ratio(3, 0.5, prior)  # raw ratio 6
        big, p_big = outliers.shrunk_rate_ratio(3000, 1500, prior)  # raw ratio 2
        self.assertLess(small, big)
        self.assertGreater(p_big, 0.99)

    def test_cusum_detects_shift(self):
        series = [100.0] * 20 + [130.0] * 10
        alarms = outliers.cusum(series, target=100, k=10, h=50)
        self.assertTrue(alarms and 20 <= alarms[0] <= 24)

    def test_bunching_below_threshold(self):
        rng = np.random.default_rng(5)
        base = rng.uniform(5000, 25000, 40000)
        steered = rng.uniform(14000, 14999, 1500)  # pushed under a $15,000 limit
        clean = outliers.bunching(list(base), 15000, 500)
        dirty = outliers.bunching(list(base) + list(steered), 15000, 500)
        self.assertLess(abs(clean.ratio), 0.1)
        self.assertGreater(dirty.ratio, 0.5)

    def test_gini(self):
        self.assertAlmostEqual(outliers.gini([1, 1, 1, 1]), 0.0)
        self.assertGreater(outliers.gini([0, 0, 0, 100]), 0.7)


class TestBids(unittest.TestCase):
    def test_collusive_tender_screens(self):
        competitive = bids.tender_screens([100, 108, 115, 121, 133])
        collusive = bids.tender_screens([100, 112, 112.5, 113, 113.4])
        self.assertLess(collusive.cv, competitive.cv)
        self.assertGreater(collusive.rd, competitive.rd)

    def test_rotation(self):
        rot = ["A", "B", "C", "D"] * 6
        obs, p = bids.rotation_test(rot)
        self.assertEqual(obs, 0)
        self.assertLess(p, 0.05)
        m = bids.win_share_matrix([{"A": 1, "B": 2}, {"A": 3, "B": 2}])
        self.assertEqual(m["A"]["B"], 1)


class TestLinkage(unittest.TestCase):
    def test_em_recovers_parameters(self):
        rng = random.Random(11)
        true_m = [0.95, 0.9, 0.85]
        true_u = [0.05, 0.2, 0.01]
        gammas = []
        for _ in range(5000):
            match = rng.random() < 0.2
            pr = true_m if match else true_u
            gammas.append([int(rng.random() < q) for q in pr])
        fit = linkage.fit_em(["name", "zip", "phone"], gammas)
        self.assertAlmostEqual(fit.p, 0.2, delta=0.03)
        for a, b in zip(fit.m, true_m):
            self.assertAlmostEqual(a, b, delta=0.05)
        self.assertGreater(fit.match_probability([1, 1, 1]), 0.99)
        self.assertLess(fit.match_probability([0, 1, 0]), 0.05)

    def test_threshold_and_jaro(self):
        scored = [(10, True), (9, True), (8, True), (7, False), (6, True), (2, False), (1, False)]
        self.assertEqual(linkage.thresholds_for_precision(scored, 0.8), 6)
        self.assertAlmostEqual(linkage.jaro_winkler("MARTHA", "MARHTA"), 0.9611, places=3)


class TestNetwork(unittest.TestCase):
    def test_hub_discount_and_components(self):
        attrs = {
            "e1": {"ph:555", "addr:1 Main"},
            "e2": {"ph:555"},
            "e3": {"addr:1 Main"},
            "e4": {"agent:RA"},
            "e5": {"agent:RA"},
        }
        edges = network.shared_attribute_edges(attrs, benign={"agent:RA"})
        self.assertNotIn(("e4", "e5"), edges)
        comps = network.components(edges)
        self.assertEqual(comps[0], {"e1", "e2", "e3"})

    def test_pagerank_from_seeds(self):
        edges = {("bad", "a"): 1.0, ("a", "b"): 1.0, ("b", "c"): 1.0, ("x", "y"): 1.0}
        r = network.personalized_pagerank(edges, {"bad"})
        self.assertGreater(r["a"], r["b"])
        self.assertGreater(r["b"], r["c"])
        self.assertAlmostEqual(r["x"], 0.0)
        self.assertAlmostEqual(sum(r.values()), 1.0, places=6)

    def test_colocation(self):
        self.assertLess(network.colocation_excess(12, 1.5), 1e-6)
        self.assertGreater(network.colocation_excess(2, 1.5), 0.3)


class TestSampling(unittest.TestCase):
    def test_stratified_hand_calc(self):
        s = [sampling.Stratum(1000, [0, 0, 10, 0, 20], X=500000), sampling.Stratum(100, [100, 0], X=200000)]
        est = sampling.stratified_total(s, 0.95)
        self.assertAlmostEqual(est.total, 1000 * 6 + 100 * 50)
        var = 1000**2 * (1 - 5 / 1000) * 80 / 5 + 100**2 * (1 - 2 / 100) * 5000 / 2
        self.assertAlmostEqual(est.se, math.sqrt(var))
        self.assertAlmostEqual(est.rate, 11000 / 700000)

    def test_ratio_estimator_coverage(self):
        # Improper dollars are skewed (most payments are correct), so normal
        # intervals under-cover at small n. This is documented in
        # forensic_methods.md section 10.3; the test pins that behavior.
        rng = np.random.default_rng(9)
        N = 20000
        paid = rng.lognormal(6, 1, N)
        err = (rng.random(N) < 0.08) * paid * rng.uniform(0.2, 1, N)
        true_rate = err.sum() / paid.sum()

        def coverage(n, reps=400):
            hit = 0
            for _ in range(reps):
                idx = rng.choice(N, n, replace=False)
                s = sampling.Stratum(N, list(err[idx]), list(paid[idx]), X=float(paid.sum()))
                e = sampling.combined_ratio([s], 0.90)
                hit += e.rate_lower <= true_rate <= e.rate_upper
            return hit / reps

        small, large = coverage(100), coverage(1500)
        self.assertLess(small, 0.85)
        self.assertGreater(large, 0.84)
        self.assertLess(small, large)

    def test_mus(self):
        self.assertAlmostEqual(sampling.poisson_upper(0, 0.95), 2.9957, places=3)
        self.assertAlmostEqual(sampling.poisson_upper(1, 0.95), 4.7439, places=3)
        self.assertAlmostEqual(sampling.mus_upper_error_limit(1_000_000, 100, []), 29957, delta=5)
        uel = sampling.mus_upper_error_limit(1_000_000, 100, [0.5])
        self.assertAlmostEqual(uel, 10000 * (2.9957 + (4.7439 - 2.9957) * 0.5), delta=5)
        self.assertEqual(sampling.mus_sample_size(1_000_000, 50_000), 60)

    def test_sizes(self):
        self.assertEqual(sampling.sample_size_proportion(0.5, 0.05), 385)
        self.assertEqual(sampling.neyman_allocation([1000, 100], [10, 100], 100), [50, 50])


class TestScoring(unittest.TestCase):
    def test_lr_and_posterior(self):
        lr = scoring.likelihood_ratio(40, 100, 500, 100000)
        self.assertGreater(lr, 50)
        post = scoring.posterior_probability(0.001, [lr])
        self.assertGreater(post, 0.05)
        self.assertLess(post, 0.5)  # still most likely innocent: base rates matter

    def test_lift_and_ap(self):
        scores = list(range(100))
        labels = [i >= 95 for i in range(100)]
        self.assertAlmostEqual(scoring.lift_at(scores, labels, 0.05), 20.0)
        self.assertAlmostEqual(scoring.average_precision(scores, labels), 1.0)
        self.assertAlmostEqual(scoring.precision_at_k(scores, labels, 10), 0.5)

    def test_two_signal_rule(self):
        groups = {"shared_phone": "network", "shared_addr": "network", "peer_outlier": "billing"}
        self.assertFalse(scoring.two_signal_rule({"shared_phone": True, "shared_addr": True}, groups).lead)
        self.assertTrue(scoring.two_signal_rule({"shared_phone": True, "peer_outlier": True}, groups).lead)


if __name__ == "__main__":
    unittest.main()
