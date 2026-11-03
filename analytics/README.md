# analytics

Reference code for the methods in the planning documents. Python 3.11+ with
NumPy; no other dependencies.

- `forensic/`: one module per family of tests in the
  [forensic methods handbook](../docs/playbook/forensic_methods.md) (digit
  tests, duplicates and splits, outliers and bunching, bid screens, record
  linkage, networks, sampling and estimation, scoring). Small and readable
  on purpose: they define the math that production pipelines must reproduce.
- `tests/`: 30 unit tests on **synthetic data only**. No real entity, payee
  or agency record appears in them, and none of their numbers is a finding.
- `universe/build_universe.py`: builds `docs/universe/data/all_agencies.csv`
  (every federal body, its tier and its screens) from the USAspending agency
  list and the classification set out in
  [the all-agency plan](../docs/universe/all_agencies.md).

Run from the repository root:

```sh
python3 -m unittest discover -s analytics/tests -t analytics
python3 analytics/universe/build_universe.py
```
