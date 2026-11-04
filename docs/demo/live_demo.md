# Live demo: the methods on real public data

**Status:** Draft v0.1 (2026-11-04), for Steve's review. Extension 8 of 10
(see the [extensions overview](../extensions.md)). Code:
`analytics/demo/run_demo.py` (scores) and
`analytics/demo/fetch_usaspending.py` (pulls awards); results:
`docs/demo/data/demo.json`; shown on the site at `/demo/`.

## Bottom line

The site's tool pages were wireframes with sample records. The demo
replaces "imagine this" with "here it is": the same reference code that
the forensic methods handbook describes, run on real public data, with the
results on a page. It deliberately starts with a dataset where the honest
answer is "nothing to see", because the most important thing to show a
leader is that the tests know their own limits.

What runs today, on data committed to the repo:

1. **Digit test on every agency's FY2026 outlays, budget authority and
   obligations** (USAspending). 301 amounts from 101 agencies.
2. **Concentration** of federal outlays across agencies.
3. **Reconciliation:** agencies whose obligations or outlays exceed budget
   authority by more than 5%.
4. **The ROI model** on GAO's FY2025 improper payment figures.

What runs where the network allows (the "Demo data" GitHub Actions
workflow, or a laptop): contract awards for any agency from the
USAspending API, scored with the digit test, a round-number test,
bunching below the simplified acquisition threshold and recipient
concentration.

## 1. Results on agency totals

| Test | Result | Reading |
| --- | --- | --- |
| First-digit test, all three amounts pooled (n = 301) | Chi-square p = 0.024; MAD 0.0195 ("nonconformity" on Nigrini's scale); spike at digit 3 | **A false positive, and a useful one.** The three amounts per agency are near-copies of each other, so the 301 values are really about 100 independent numbers counted three times; that inflates the chi-square. Benford tests assume many independent transactions |
| First-digit test, outlays only (n = 101) | Chi-square p = 0.20; MAD 0.031 | No evidence against Benford. The MAD still reads "nonconformity" because Nigrini's MAD ranges assume thousands of records; at n = 101, MAD is mostly noise. This is why the handbook sets a minimum of 1,000 records |
| Concentration | Gini 0.94; top five agencies 85% of outlays, top ten 94% | Expected: Social Security, health, Treasury and defense dominate. Context for the scorecard, not a fraud signal |
| Reconciliation | No agency with more than $100M in budget authority shows obligations or outlays more than 5% above it | Clean at this level. Agency-level totals are reconciled before publication; the test earns its keep at the program and award level |

The page shows the observed and expected digit distributions side by side
so a viewer can see what a "pass" looks like before seeing a "flag".

## 2. Award-level demo (when run with network access)

`fetch_usaspending.py` pulls the most recent contract awards for one agency
and year (sorted by date, not size, so the sample is not only the largest
awards). `run_demo.py` then reports, for each file:

- first-digit test (when there are at least 100 awards);
- share of awards that are round thousands;
- bunching below the simplified acquisition threshold (when at least 200
  awards fall between half and one and a half times it);
- number of recipients, Herfindahl index and the top-ten recipient share.

No recipient is named on the page. Award-level results are statistics on
public records, for showing the method, not leads.

## 3. How to refresh

```
python3 analytics/roi/model.py
python3 analytics/demo/run_demo.py
# with network access to api.usaspending.gov:
python3 analytics/demo/fetch_usaspending.py \
  --agency "Department of Veterans Affairs" --fy 2025
python3 analytics/demo/run_demo.py
```

Or run the **Demo data** workflow from the repository's Actions tab; it
uploads `docs/demo/data/` as an artifact to commit.

## 4. Next demos

1. CMS hospice enrollment and owner files through the network scorer
   (HHS-1), once the public files are pulled.
2. SAM.gov exclusions matched to USAspending recipients (cross-agency
   matching, business side).
3. Single Audit repeat findings for the largest pass-through programs.
