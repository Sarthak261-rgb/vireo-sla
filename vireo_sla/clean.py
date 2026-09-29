"""Load and clean the Vireo export. Every rule here is a decision documented in DECISIONS.md."""
import pandas as pd

IST_OFFSET = pd.Timedelta(minutes=330)
# Policy s3 first-response targets, minutes.
TARGET_MIN = {"chat": 15, "voice": 120, "social": 240, "email": 480}
# Policy s2: social is worked by Chat Frontline. Used to decide which roster covers a ticket.
CHANNEL_TEAM = {"chat": "Chat Frontline", "social": "Chat Frontline",
                "email": "Email Frontline", "voice": "Voice Frontline"}
CREDIT_INR = 350  # policy s3
SHIFTS = ("Morning", "Day", "Night")


def shift_of_hour(h):
    """Policy s7, IST: Morning 06-14, Day 14-22, Night 22-06."""
    return "Morning" if 6 <= h < 14 else "Day" if 14 <= h < 22 else "Night"


def load_roster(path):
    a = pd.read_csv(path, parse_dates=["from_date", "to_date"])
    a["to_date"] = a["to_date"].fillna(pd.Timestamp("2099-12-31"))  # blank = still active
    return a


def load_tickets(path):
    """Returns (clean_tickets, quality_log). quality_log is a list of (check, count, action)."""
    t = pd.read_csv(path, parse_dates=["created_at", "first_response_at", "resolved_at"])
    log = [("rows in export", len(t), "")]

    # 1. Migration re-import: same ticket_id in both systems. Keep the helpdesk row
    #    (csat blank = no response; legacy csat 0 = no response, README).
    dup = t.ticket_id.duplicated(keep=False)
    drop = dup & (t.source_system == "legacy_fd")
    log.append(("ticket_ids present twice (helpdesk + legacy_fd)", int(dup.sum() // 2),
                "kept helpdesk copy, dropped legacy copy"))
    t = t[~drop].copy()
    left = int(t.ticket_id.duplicated().sum())
    log.append(("duplicate ticket_ids remaining", left, "none expected"))

    # 2. Timestamps are UTC (README). Shifts and weeks are IST (policy s7).
    for c in ("created_at", "first_response_at", "resolved_at"):
        t[c + "_ist"] = t[c] + IST_OFFSET
    voice_hours = t.loc[t.channel == "voice", "created_at_ist"].dt.hour
    log.append(("voice tickets created outside 08:00-22:00 IST (validates UTC->IST)",
                int(((voice_hours < 8) | (voice_hours >= 22)).sum()), "expected 0"))

    # 3. CSAT: 0 (legacy) and blank both mean "no response". Never average zeros.
    t["csat"] = t.csat_score.where(t.csat_score > 0)

    # 4. First-response metrics.
    t["frt_min"] = (t.first_response_at - t.created_at).dt.total_seconds() / 60
    log.append(("tickets with no first response", int(t.frt_min.isna().sum()), "excluded from breach rate"))
    log.append(("first response before creation", int((t.frt_min < 0).sum()), "excluded"))
    t = t[t.frt_min.notna() & (t.frt_min >= 0)].copy()
    t["target_min"] = t.channel.map(TARGET_MIN)
    t["breach"] = t.frt_min > t.target_min
    # Policy s3: the credit is issued on resolution, so only resolved/closed tickets cost money.
    t["credit_inr"] = (t.breach & t.status.isin(["resolved", "closed"])) * CREDIT_INR

    # 5. Shift the ticket was CREATED in (IST) - this is when the queue needed cover.
    t["created_shift"] = t.created_at_ist.dt.hour.map(shift_of_hour)
    t["week"] = t.created_at_ist.dt.to_period("W-SUN").dt.start_time  # Monday of the IST week
    return t, log
