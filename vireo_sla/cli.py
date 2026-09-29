import argparse
import sys
import pandas as pd
from .clean import load_tickets, load_roster
from .attribute import add_roster_context
from .report import build


def main(argv=None):
    ap = argparse.ArgumentParser(description="Vireo first-response SLA breach report")
    ap.add_argument("--data", default="data", help="folder with tickets.csv and agents.csv")
    ap.add_argument("--out", default="out", help="output folder")
    ap.add_argument("--week", help="Monday (YYYY-MM-DD) of the week to report as-of; default = latest week in data")
    a = ap.parse_args(argv)
    t, log = load_tickets(f"{a.data}/tickets.csv")
    t = add_roster_context(t, load_roster(f"{a.data}/agents.csv"))
    h, fl = build(t, log, a.out, pd.Timestamp(a.week) if a.week else None)
    print(f"Report written to {a.out}/report.html")
    print(f"Last {h['quarters']} quarters: breach rate {h['breach_rate']*100:.1f}% ; "
          f"{h['gap_share_of_breaches']*100:.0f}% of breaches on tickets created with no cover; "
          f"avoidable credits ~Rs {h['avoidable_credit_inr_per_quarter']:,}/quarter; "
          f"agents flagged: {int(fl.flag.sum())} of {len(fl)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
