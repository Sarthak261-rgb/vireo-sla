"""Writes CSVs + a single self-contained HTML report (no JavaScript, opens anywhere)."""
import html
import json
import pandas as pd
from .metrics import (weekly_by_shift, weekly_by_resolver_shift, weekly_by_agent, agent_flags,
                      coverage_gaps, quarterly, headline, rate, ROLLING_WEEKS, MIN_N_FLAG, FLAG_ALPHA)


def _table(df, cls=""):
    return df.to_html(index=False, border=0, classes=cls, escape=True, na_rep="")


def _pct(x):
    return f"{x*100:.1f}%"


def _inr(x):
    return f"Rs {x:,.0f}"


def build(t, log, out_dir, as_of_week=None):
    import os
    os.makedirs(out_dir, exist_ok=True)
    last_day = t.created_at_ist.max().normalize()
    # default: the last COMPLETE Monday-Sunday week, so a 2-day stub week never looks like a trend
    as_of = as_of_week or (t.week.max() if last_day.weekday() == 6 else t.week.max() - pd.Timedelta(weeks=1))
    ws, wr, wa = weekly_by_shift(t), weekly_by_resolver_shift(t), weekly_by_agent(t)
    fl, cg, q, h = agent_flags(t, as_of), coverage_gaps(t), quarterly(t), headline(t)
    ws.to_csv(f"{out_dir}/weekly_by_shift.csv", index=False)
    wr.to_csv(f"{out_dir}/weekly_by_resolver_shift_helpdesk_view.csv", index=False)
    wa.to_csv(f"{out_dir}/weekly_by_agent.csv", index=False)
    fl.to_csv(f"{out_dir}/agent_flags.csv", index=False)
    cg.to_csv(f"{out_dir}/coverage_gaps.csv", index=False)
    q.to_csv(f"{out_dir}/quarterly.csv", index=False)
    pd.DataFrame(log, columns=["check", "count", "action"]).to_csv(f"{out_dir}/data_quality.csv", index=False)
    json.dump(h, open(f"{out_dir}/headline.json", "w"), indent=2, default=str)

    # --- helpdesk view vs cause view, last 12 weeks pooled
    recent = t[t.week > as_of - pd.Timedelta(weeks=12)]
    recent = recent[recent.week <= as_of]
    hv = recent.groupby("resolver_shift").agg(breaches=("breach", "sum")).reset_index()
    hv["from_overnight_gap"] = [int(((recent.resolver_shift == s) & (recent.cause == "coverage gap") & recent.breach).sum())
                                for s in hv.resolver_shift]
    hv["own_shift_breaches"] = hv.breaches - hv.from_overnight_gap
    hv = hv.rename(columns={"resolver_shift": "shift (resolver)", "breaches": "breaches charged (helpdesk view)",
                            "from_overnight_gap": "of which created overnight with no cover",
                            "own_shift_breaches": "of which genuinely on-shift"})

    wk = ws[(ws.week <= as_of) & (ws.week > as_of - pd.Timedelta(weeks=8))].pivot_table(
        index="week", columns="cause", values=["tickets", "breaches"], aggfunc="sum", fill_value=0)
    wk.columns = [f"{a} ({b})" for a, b in wk.columns]
    wk = wk.reset_index()
    wk["week"] = wk.week.dt.strftime("%d %b %Y")

    flagged = fl[fl.flag]
    fl_show = fl.head(8)[["name", "team", "shift", "in_shift_tickets", "in_shift_breaches", "in_shift_rate", "p_value", "flag"]]
    flag_sentence = (f"{len(flagged)} of {len(fl)} agents are statistically above the desk's on-shift breach rate "
                     f"(threshold: at least {MIN_N_FLAG} on-shift tickets in {ROLLING_WEEKS} weeks and p&lt;{FLAG_ALPHA}). "
                     + ("Names: " + ", ".join(flagged.name) + "." if len(flagged) else
                        "There is nobody to have a performance conversation with on this measure."))
    cur = quarterly(t).iloc[-1]
    css = ("body{font:15px/1.5 system-ui,Segoe UI,Arial;max-width:980px;margin:24px auto;padding:0 16px;color:#1a1a1a}"
           "h1{font-size:22px}h2{font-size:17px;margin-top:28px}table{border-collapse:collapse;font-size:13px;margin:8px 0}"
           "td,th{padding:4px 10px;border-bottom:1px solid #ddd;text-align:right}th{background:#f3f3f3}td:first-child,th:first-child{text-align:left}"
           ".big{background:#fff6e0;border-left:4px solid #e0a000;padding:10px 14px}.small{color:#666;font-size:12px}")
    body = f"""<h1>Vireo Audio: first-response SLA breach report</h1>
<p class=small>Latest complete week ending {(as_of + pd.Timedelta(days=6)).date()} (IST). Data window {t.created_at_ist.min().date()} to {t.created_at_ist.max().date()}.
Cleaned tickets: {len(t):,}.</p>
<div class=big><b>The one-line finding.</b> Tickets created in a window where nobody from the channel's frontline team was
rostered ({h['gap_tickets']:,} tickets, {h['gap_tickets']/h['tickets']*100:.0f}% of volume in the last {h['quarters']} quarters) account for
<b>{h['gap_breaches']:,} of {h['breaches']:,} breaches ({_pct(h['gap_share_of_breaches'])})</b>. Every other ticket breaches at a flat
{_pct(h['in_shift_breach_rate'])}. Restoring overnight cover would take the breach rate from {_pct(h['breach_rate'])} to about
{_pct(h['breach_rate_if_fixed'])} and avoid about {_inr(h['avoidable_credit_inr_per_quarter'])} of credits per quarter (at export volume).</div>

<h2>1. Which shift is breaching most, as the helpdesk counts it vs. where the breach began (last 12 weeks)</h2>
{_table(hv)}
<p class=small>The helpdesk charges a breach to whoever resolves the ticket. Overnight tickets are picked up and closed by the Morning
shift (policy s7), so Morning looks worst while the cause is that nobody was on at night.</p>

<h2>2. Weekly trend, last 8 weeks</h2>
{_table(wk)}

<h2>3. Coverage gaps (created with no rostered agent from the channel's frontline team)</h2>
{_table(cg.assign(first_seen=cg.first_seen.dt.strftime('%Y-%m-%d %H:%M')))}

<h2>4. Agents: on-shift breach rate, rolling {ROLLING_WEEKS} weeks, 8 lowest p-values</h2>
<p>{flag_sentence}</p>
{_table(fl_show)}
<p class=small>Full weekly agent table: weekly_by_agent.csv. A typical agent resolves about 3 tickets a week, so a single week says nothing
about a person; that is why this view is rolling. Tier 2 (Escalations &amp; Warranty) is listed but never flagged (policy s6).</p>

<h2>5. Quarterly view</h2>
{_table(q)}
<p class=small>Credits are issued on resolution (policy s3), so open/pending breaches are not yet costed.
CSAT on breached tickets averages {h['csat_breached']} vs {h['csat_ok']} otherwise ({h['csat_responses']:,} responses; blanks and legacy zeros excluded).</p>

<h2>6. Data checks applied</h2>
{_table(pd.DataFrame(log, columns=['check', 'count', 'action']))}
"""
    open(f"{out_dir}/report.html", "w", encoding="utf-8").write(
        f"<!doctype html><meta charset=utf-8><title>Vireo SLA report</title><style>{css}</style>{body}")
    return h, fl
