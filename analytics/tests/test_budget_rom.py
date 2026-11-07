"""Checks on the agency budget and fraud ROM allocation
(analytics/universe/budget_fraud_rom.py). Reads the committed agency list;
writes nothing.

Run from the repo root:  python3 -m unittest discover -s analytics/tests -t analytics
"""
import unittest

from universe import budget_fraud_rom as rom


class TestBudgetRom(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = rom.build()

    def test_every_body_listed_once(self):
        abbrs = [r["abbreviation"] for r in self.rows]
        self.assertEqual(len(abbrs), 137)
        self.assertEqual(len(set(abbrs)), 137)

    def test_totals_equal_gao_range(self):
        self.assertAlmostEqual(sum(r["fraud_rom_low_usd"] for r in self.rows), rom.GAO_LOW, delta=1)
        self.assertAlmostEqual(sum(r["fraud_rom_high_usd"] for r in self.rows), rom.GAO_HIGH, delta=1)

    def test_unscored_rows_get_nothing(self):
        for r in self.rows:
            if r["risk_class"] == "-":
                self.assertEqual(r["fraud_rom_high_usd"], 0)

    def test_treasury_interest_removed(self):
        t = next(r for r in self.rows if r["abbreviation"] == "TREAS")
        self.assertAlmostEqual(float(t["budget_usd"]) - t["exposed_usd"], rom.TREAS_INTEREST_EXCLUDED, delta=1)


if __name__ == "__main__":
    unittest.main()
