"""Join tickets to the roster and decide WHY each breach happened."""
import pandas as pd
from .clean import CHANNEL_TEAM


def shift_date(ts):
    """Roster dates are shift start dates: a 01:00 IST ticket belongs to the Night shift that began
    at 22:00 the previous calendar day (roster to_date 2025-06-29 covers that night until 06:00 on the 30th)."""
    return (ts - pd.to_timedelta((ts.dt.hour < 6) * 1, unit="D")).dt.normalize()


def add_roster_context(t, roster):
    """Adds resolver_shift/resolver_tier/resolver_name (roster row effective on first-response date)
    and staffed_at_creation (was anyone from the channel's frontline team rostered on the
    shift the ticket was created in, on that date?)."""
    t = t.copy()
    d_resp = shift_date(t.first_response_at_ist)
    m = t[["ticket_id", "agent_id"]].assign(d=d_resp).merge(roster, on="agent_id", how="left")
    m = m[(m.from_date <= m.d) & (m.to_date >= m.d)].drop_duplicates("ticket_id")
    m = m.set_index("ticket_id")
    t["resolver_name"] = t.ticket_id.map(m["name"])
    t["resolver_shift"] = t.ticket_id.map(m["shift"])
    t["resolver_team"] = t.ticket_id.map(m["team"])
    t["resolver_tier"] = t.ticket_id.map(m["tier"])

    # Coverage table: (team, shift) -> list of (from, to) intervals with >=1 agent rostered.
    d_created = shift_date(t.created_at_ist)
    team = t.channel.map(CHANNEL_TEAM)
    days = pd.DataFrame({"team": team, "shift": t.created_shift, "d": d_created}).drop_duplicates()
    cnt = days.merge(roster, left_on=["team", "shift"], right_on=["team", "shift"], how="left")
    cnt = cnt[(cnt.from_date <= cnt.d) & (cnt.to_date >= cnt.d)].groupby(["team", "shift", "d"]).size()
    key = pd.MultiIndex.from_arrays([team, t.created_shift, d_created])
    t["staffed_at_creation"] = pd.Series(cnt.reindex(key).fillna(0).values, index=t.index) > 0
    # Voice is only accepted 08-22 IST (policy s2), so a voice ticket is never in an unstaffed window.
    t["cause"] = "in-shift"
    t.loc[~t.staffed_at_creation, "cause"] = "coverage gap"
    return t


def unmatched_report(t):
    return int(t.resolver_shift.isna().sum())
