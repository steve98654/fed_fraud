"""Pull contract awards for one agency and fiscal year from the public
USAspending API, for the live demo (docs/demo/live_demo.md).

Needs outbound HTTPS to api.usaspending.gov; standard library only. Run it
where that host is reachable (a laptop, or the "Demo data" GitHub Actions
workflow), then run run_demo.py to score the result.

    python3 analytics/demo/fetch_usaspending.py --agency "Department of Veterans Affairs" --fy 2025 --max 5000

Writes docs/demo/data/awards_<slug>_<fy>.csv with one row per award. These
are public records published by the government; the demo reports only
aggregate test results and never names a recipient as a lead.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
FIELDS = ["Award ID", "Recipient Name", "Award Amount", "Start Date", "Awarding Sub Agency", "NAICS", "Contract Award Type"]
CONTRACTS = ["A", "B", "C", "D"]  # BPA call, purchase order, delivery order, definitive contract


def fetch(agency: str, fy: int, max_rows: int, page_size: int = 100, pause: float = 0.3) -> list[dict]:
    rows: list[dict] = []
    page = 1
    while len(rows) < max_rows:
        body = {
            "filters": {
                "award_type_codes": CONTRACTS,
                "time_period": [{"start_date": f"{fy - 1}-10-01", "end_date": f"{fy}-09-30"}],
                "agencies": [{"type": "awarding", "tier": "toptier", "name": agency}],
            },
            "fields": FIELDS,
            "page": page,
            "limit": page_size,
            "sort": "Start Date",  # by date, not amount, so the sample is not only the largest awards
            "order": "desc",
        }
        req = urllib.request.Request(API, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
        batch = data.get("results", [])
        rows.extend(batch)
        if not batch or not data.get("page_metadata", {}).get("hasNext"):
            break
        page += 1
        time.sleep(pause)
    return rows[:max_rows]


def main() -> Path:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agency", required=True, help='toptier agency name, e.g. "Department of Veterans Affairs"')
    ap.add_argument("--fy", type=int, required=True)
    ap.add_argument("--max", type=int, default=5000)
    a = ap.parse_args()
    rows = fetch(a.agency, a.fy, a.max)
    slug = re.sub(r"[^a-z0-9]+", "-", a.agency.lower()).strip("-")
    out = ROOT / f"docs/demo/data/awards_{slug}_{a.fy}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["award_id", "recipient", "amount", "start_date", "sub_agency", "naics", "award_type"])
        for r in rows:
            naics = r.get("NAICS")
            if isinstance(naics, dict):
                naics = naics.get("code", "")
            w.writerow([r.get("Award ID"), r.get("Recipient Name"), r.get("Award Amount"), r.get("Start Date"),
                        r.get("Awarding Sub Agency"), naics or "", r.get("Contract Award Type") or ""])
    print(f"{len(rows)} awards -> {out.relative_to(ROOT)}")
    return out


if __name__ == "__main__":
    main()
