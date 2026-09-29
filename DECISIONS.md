# Decisions (things the pack left open, what I chose, why)

| # | Question | Decision | Why |
|---|---|---|---|
| 1 | Timestamps: UTC or IST? | UTC (README). Convert to IST (+05:30) before shifts and weeks. | Voice callbacks only run 08:00-22:00 IST (policy s2). After conversion 0 voice tickets fall outside that window. Reading UTC as IST puts 68% of tickets in the wrong shift. |
| 2 | Duplicate ticket_ids (616) | Keep the `helpdesk` copy, drop `legacy_fd`. | The two rows differ only in source_system (and csat 0 vs blank). The helpdesk copy has the correct blank csat. |
| 3 | CSAT 0 | Treat as no response. | README + policy s8. Never average zeros. |
| 4 | What is "breach"? | first_response - created > target, strictly. | Policy s3 "later than the target". Boundary is unit-tested. |
| 5 | Who owns a breach? | Report **both** the helpdesk view (resolver) and a cause view; lead with cause. | Policy s3 charges the resolver; s7 says the night queue is picked up by the next shift, so Morning is charged for tickets that arrived while nobody was on. The export has no first-responder id, so the resolver is the only agent available. |
| 6 | Which shift is a ticket "in"? | The shift it was **created** in (IST); a 01:00 ticket belongs to the previous day's Night shift. | Coverage fails when the ticket arrives, not when it is closed. Roster dates are shift-start dates (to_date 29 Jun covers the night to 06:00 on 30 Jun). |
| 7 | When is a window "uncovered"? | No agent rostered on that (team, shift, date), where team = the channel's frontline team (chat and social -> Chat Frontline, email -> Email Frontline, voice -> Voice Frontline). | My first attempt used the ticket's `assigned_team` (Billing, Logistics...). Those teams never had night staff, even in H1 2025 when night tickets were answered fine by the Indore night frontline, so it wrongly flagged pre-June tickets. Frontline-by-channel matches the data. |
| 8 | Weekly per-agent ranking? | Provide the table, but flag people only on a rolling 8-week on-shift rate with a significance test; never flag Tier 2. | The median agent resolves 3 tickets a week; one week is noise. Policy s6: Tier 2 is not comparable on volume. With this rule 0 of 41 agents are flagged, and I say so rather than manufacture a list. |
| 9 | Credit cost | Rs 350 x breached tickets that are resolved or closed. | Policy s3: issued on resolution. |
| 10 | Headline counterfactual | Gap tickets would breach at the in-shift rate for their channel. | The in-shift rate is flat at 8.9-10.0% in every quarter, before and after the change. |
| 11 | Partial last week | Report as-of the last complete Mon-Sun week. | 30 Jun 2026 is a Tuesday; a 2-day stub looks like a collapse. |
| 12 | Headcount | The recommendation is a reassignment, not a hire. | Arjun (Finance): frozen till Q4. |
| 13 | Volume mismatch | Headline is at export volume (~172 tickets/week); a scaled figure is shown separately. | The brief says ~650/week. I cannot tell whether the export is a sample. The conservative number leads. |
| 14 | LLM at runtime? | None. | The findings come from timestamps and the roster. The free text did not explain breaches (no keyword I tried moved the breach rate much), and an LLM narrative adds cost and a way to be confidently wrong in a report whose purpose is to be trusted. |
