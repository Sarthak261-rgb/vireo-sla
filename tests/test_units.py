import unittest
import pandas as pd
from vireo_sla.clean import load_tickets, shift_of_hour
from vireo_sla.attribute import add_roster_context, shift_date

COLS = ["ticket_id", "created_at", "first_response_at", "resolved_at", "status", "channel", "customer_id", "order_id",
        "product_sku", "category", "priority", "assigned_team", "agent_id", "transfers", "csat_score",
        "refund_amount_inr", "refund_reason_code", "replacement_issued", "customer_message", "agent_notes",
        "source_system"]


def mk(tmp, rows):
    df = pd.DataFrame(rows, columns=COLS)
    p = f"{tmp}/t.csv"
    df.to_csv(p, index=False)
    return p


def row(tid, created, fr, ch="chat", agent="A1", src="helpdesk", csat=None, status="resolved"):
    return [tid, created, fr, "2025-08-01 12:00", status, ch, "C1", None, "VA-EB-PL1", "Other", "Normal",
            "Chat Frontline", agent, 0, csat, None, None, "N", "msg", "note", src]


class Units(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.d = tempfile.mkdtemp()

    def test_utc_to_ist_and_shift(self):
        # 16:30 UTC = 22:00 IST -> Night, not Day
        t, _ = load_tickets(mk(self.d, [row("T1", "2025-08-01 16:30", "2025-08-01 16:40")]))
        self.assertEqual(t.created_shift.iloc[0], "Night")
        self.assertEqual(shift_of_hour(5), "Night"); self.assertEqual(shift_of_hour(6), "Morning")
        self.assertEqual(shift_of_hour(13), "Morning"); self.assertEqual(shift_of_hour(14), "Day")

    def test_breach_boundary_is_strictly_later_than_target(self):
        t, _ = load_tickets(mk(self.d, [row("T1", "2025-08-01 05:00", "2025-08-01 05:15"),
                                        row("T2", "2025-08-01 05:00", "2025-08-01 05:16")]))
        self.assertEqual(list(t.breach), [False, True])

    def test_dedupe_keeps_helpdesk_and_csat_zero_is_blank(self):
        t, _ = load_tickets(mk(self.d, [row("T1", "2025-08-01 05:00", "2025-08-01 05:05", src="legacy_fd", csat=0),
                                        row("T1", "2025-08-01 05:00", "2025-08-01 05:05", src="helpdesk"),
                                        row("T2", "2025-08-01 05:00", "2025-08-01 05:05", src="legacy_fd", csat=0)]))
        self.assertEqual(len(t), 2)
        self.assertEqual(t[t.ticket_id == "T1"].source_system.iloc[0], "helpdesk")
        self.assertTrue(t.csat.isna().all())

    def test_credit_only_when_resolved(self):
        t, _ = load_tickets(mk(self.d, [row("T1", "2025-08-01 05:00", "2025-08-01 06:00", status="pending"),
                                        row("T2", "2025-08-01 05:00", "2025-08-01 06:00")]))
        self.assertEqual(list(t.credit_inr), [0, 350])

    def test_night_shift_date_rolls_back_before_6am(self):
        s = pd.Series(pd.to_datetime(["2025-06-30 01:00", "2025-06-30 05:59", "2025-06-30 06:00", "2025-06-30 23:00"]))
        self.assertEqual(list(shift_date(s).dt.strftime("%m-%d")), ["06-29", "06-29", "06-30", "06-30"])

    def test_roster_move_is_effective_dated(self):
        roster = pd.DataFrame([
            ["A1", "Zed", "Indore", "Chat Frontline", "Night", 1, "2021-01-01", "2025-06-29"],
            ["A1", "Zed", "Indore", "Chat Frontline", "Day", 1, "2025-06-30", "2099-12-31"]],
            columns=["agent_id", "name", "site", "team", "shift", "tier", "from_date", "to_date"])
        for c in ("from_date", "to_date"):
            roster[c] = pd.to_datetime(roster[c])
        # 23:00 IST on 29 Jun (Night, still rostered) vs 23:00 IST on 1 Jul (Night, nobody)
        t, _ = load_tickets(mk(self.d, [row("T1", "2025-06-29 17:30", "2025-06-29 17:35"),
                                        row("T2", "2025-07-01 17:30", "2025-07-01 17:35")]))
        t = add_roster_context(t, roster)
        self.assertEqual(list(t.cause), ["in-shift", "coverage gap"])
        self.assertEqual(t.resolver_shift.iloc[0], "Night")


if __name__ == "__main__":
    unittest.main()
