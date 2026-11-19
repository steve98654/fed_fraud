# analytics

Reference code for the methods in the planning documents. Python 3.11+ with
NumPy; no other dependencies.

- `forensic/`: one module per family of tests in the
  [forensic methods handbook](../docs/playbook/forensic_methods.md) (digit
  tests, duplicates and splits, outliers and bunching, bid screens, record
  linkage, networks, sampling and estimation, scoring), plus the extension
  screens: `crossmatch.py` (cross-agency identity matching), cluster
  scoring in `network.py`, `procurement.py` (competition, contract growth,
  set-asides) and `passthrough.py` (grants to states). Small and readable
  on purpose: they define the math that production pipelines must reproduce.
- `roi/`: the recovery and ROI model (`model.py`) and its program inputs
  (`programs.csv`, GAO FY2025 improper payments); writes
  `docs/proposals/data/roi_results.*`.
- `triage/tips.py`: hotline tip triage, a rule baseline plus an optional
  Claude scorer (needs the `anthropic` package and an authorized deployment).
- `demo/`: the live demo. `run_demo.py` scores committed public data and any
  fetched award files into `docs/demo/data/demo.json`;
  `fetch_usaspending.py` pulls contract awards (needs network access to
  api.usaspending.gov, or run the "Demo data" workflow).
- `tests/`: 53 unit tests on **synthetic data only**. No real entity, payee
  or agency record appears in them, and none of their numbers is a finding.
- `universe/build_universe.py`: builds `docs/universe/data/all_agencies.csv`
  (every federal body, its tier and its screens) from the USAspending agency
  list and the classification set out in
  [the all-agency plan](../docs/universe/all_agencies.md).
- `universe/budget_fraud_rom.py`: builds the agency budget and fraud ROM
  table ([budget_fraud_rom.md](../docs/universe/budget_fraud_rom.md) and
  `docs/universe/data/agency_budget_fraud_rom.csv`), sharing GAO's $233B to
  $521B government-wide estimate across agencies by risk-weighted outlays.

Run from the repository root:

```sh
python3 -m unittest discover -s analytics/tests -t analytics
python3 analytics/universe/build_universe.py
python3 analytics/universe/budget_fraud_rom.py
python3 analytics/roi/model.py
python3 analytics/demo/run_demo.py
```
