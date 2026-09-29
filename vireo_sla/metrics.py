"""Aggregations, the agent flagging rule, and the headline business numbers."""
import math
import pandas as pd
from .clean import CREDIT_INR

MIN_N_FLAG = 30      # do not flag an agent on fewer in-shift tickets than this
FLAG_ALPHA = 0.01    # one-sided binomial p-value vs the desk's in-shift baseline
ROLLING_WEEKS = 8


def rate(df):
    return df.breach.mean() if len(df) else float("nan")


def weekly_by_shift(t):
    g = t.groupby(["week", "created_shift", "cause"]).agg(
        tickets=("breach", "size"), breaches=("breach", "sum")).reset_index()
    g["breach_rate"] = (g.breaches / g.tickets).round(3)
    return g


def weekly_by_resolver_shift(t):
    """What the helpdesk's standard report shows: breaches charged to the resolving agent's shift."""
    g = t.groupby(["week", "resolver_shift"]).agg(tickets=("breach", "size"), breaches=("breach", "sum"),
                                                  of_which_coverage_gap=("cause", lambda s: (s == "coverage gap").sum()))
    return g.reset_index()


def binom_upper_p(k, n, p):
    """P(X >= k) for X~Bin(n,p). Exact, no scipy."""
    return sum(math.comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k, n + 1))


def weekly_by_agent(t):
    g = t.groupby(["week", "agent_id", "resolver_name", "resolver_team", "resolver_shift", "resolver_tier"],
                  dropna=False)
    out = g.agg(tickets=("breach", "size"), breaches_helpdesk_view=("breach", "sum")).reset_index()
    gap = t[t.cause == "coverage gap"].groupby(["week", "agent_id"]).breach.sum().rename("breaches_from_coverage_gap")
    ins = t[t.cause == "in-shift"].groupby(["week", "agent_id"]).agg(
        in_shift_tickets=("breach", "size"), in_shift_breaches=("breach", "sum"))
    out = out.merge(gap, on=["week", "agent_id"], how="left").merge(ins, on=["week", "agent_id"], how="left")
    out = out.fillna({"breaches_from_coverage_gap": 0, "in_shift_tickets": 0, "in_shift_breaches": 0})
    for c in ("breaches_from_coverage_gap", "in_shift_tickets", "in_shift_breaches"):
        out[c] = out[c].astype(int)
    return out.sort_values(["week", "agent_id"])


def agent_flags(t, as_of_week=None):
    """Rolling in-shift breach rate per agent over the last ROLLING_WEEKS, flagged only when statistically
    distinguishable from the desk baseline. Tier 2 is listed but never flagged (policy s6)."""
    base = rate(t[t.cause == "in-shift"])
    as_of = as_of_week or t.week.max()
    win = t[(t.week > as_of - pd.Timedelta(weeks=ROLLING_WEEKS)) & (t.week <= as_of) & (t.cause == "in-shift")]
    rows = []
    for aid, x in win.groupby("agent_id"):
        n, k = len(x), int(x.breach.sum())
        p = binom_upper_p(k, n, base) if n else 1.0
        tier = x.resolver_tier.iloc[0]
        rows.append(dict(agent_id=aid, name=x.resolver_name.iloc[0], team=x.resolver_team.iloc[0],
                         shift=x.resolver_shift.iloc[-1], tier=tier, in_shift_tickets=n, in_shift_breaches=k,
                         in_shift_rate=round(k / n, 3), baseline=round(base, 3), p_value=round(p, 4),
                         flag=bool(tier == 1 and n >= MIN_N_FLAG and p < FLAG_ALPHA)))
    return pd.DataFrame(rows).sort_values("p_value")


def coverage_gaps(t):
    g = t[t.cause == "coverage gap"].groupby(["channel", "created_shift"]).agg(
        first_seen=("created_at_ist", "min"), tickets=("breach", "size"), breaches=("breach", "sum"))
    g["breach_rate"] = (g.breaches / g.tickets).round(3)
    return g.reset_index()


def quarterly(t):
    q = t.created_at_ist.dt.to_period("Q").astype(str)
    g = t.groupby(q).agg(tickets=("breach", "size"), breaches=("breach", "sum"), credit_inr=("credit_inr", "sum"))
    g["breach_rate"] = (g.breaches / g.tickets).round(3)
    g["gap_breaches"] = t[t.cause == "coverage gap"].groupby(q).breach.sum()
    g["gap_breaches"] = g.gap_breaches.fillna(0).astype(int)
    g["gap_share_of_breaches"] = (g.gap_breaches / g.breaches).round(3)
    return g.reset_index().rename(columns={"created_at_ist": "quarter", "index": "quarter"})


def headline(t, last_quarters=4):
    """The business number. Counterfactual: tickets created in an unstaffed window would have breached at the
    in-shift rate of the same channel (same mix of targets). Only resolved/closed tickets cost credits."""
    end = t.created_at_ist.max()
    start = (end.to_period("Q") - (last_quarters - 1)).start_time
    w = t[t.created_at_ist >= start]
    ins = t[(t.cause == "in-shift") & (t.created_at_ist >= start)]
    ins_rate = ins.groupby("channel").breach.mean()
    gap = w[w.cause == "coverage gap"]
    expected = gap.channel.map(ins_rate).sum()
    resolved_share = gap.status.isin(["resolved", "closed"]).mean() if len(gap) else 0
    avoidable = (gap.breach.sum() - expected)
    cur = t[t.created_at_ist >= (end.to_period("Q")).start_time]
    cs = w.groupby("breach").csat.mean()
    return dict(
        window=f"{start.date()} to {end.date()}", quarters=last_quarters,
        tickets=len(w), breaches=int(w.breach.sum()), breach_rate=round(w.breach.mean(), 4),
        credit_inr_total=int(w.credit_inr.sum()), credit_inr_per_quarter=round(w.credit_inr.sum() / last_quarters),
        gap_tickets=len(gap), gap_breaches=int(gap.breach.sum()),
        gap_share_of_breaches=round(gap.breach.sum() / w.breach.sum(), 3),
        in_shift_breach_rate=round(w[w.cause == "in-shift"].breach.mean(), 4),
        avoidable_breaches=round(avoidable), avoidable_credit_inr=round(avoidable * resolved_share * CREDIT_INR),
        avoidable_credit_inr_per_quarter=round(avoidable * resolved_share * CREDIT_INR / last_quarters),
        breach_rate_if_fixed=round((w.breach.sum() - avoidable) / len(w), 4),
        current_quarter_breach_rate=round(cur.breach.mean(), 4),
        csat_breached=round(cs.get(True, float("nan")), 2), csat_ok=round(cs.get(False, float("nan")), 2),
        csat_responses=int(w.csat.notna().sum()),
    )
