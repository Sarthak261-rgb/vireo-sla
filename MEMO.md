**To:** Neha Kulkarni, Support Operations Manager
**Cc:** Priya Raman, Arjun Mehta, Sameer Qureshi
**From:** Kabir Nanda's team
**Re:** SLA breach report: what it shows, and what I'd change about the question

Neha, your weekly report by agent and shift is built and attached (`out/report.html`, plus CSVs). I'd like you to read the
first finding before you use the agent view, because it changes who you should have the conversation with.

## The finding

**Seven in ten SLA breaches happen on tickets that arrived when nobody was on the desk.** Since 30 June 2025 there has been
no one rostered for chat, social or email between 10pm and 6am. The roster shows why: on 29 June 2025 three night agents left
and two moved to the Day shift, and none were replaced. Since then:

- Every chat that arrives overnight breaches (1,036 of 1,036 since 30 June). Before June only 8% did.
- Overnight social breaches 86% of the time. Overnight email breaches 50%, almost all of it emails that arrive 10pm-midnight,
  because the 8-hour clock runs out before the Morning shift starts at 6am.
- Every ticket created while a team was on shift breaches at a flat **9%**, in every quarter, before and after June 2025.
  Nothing else has moved.

## Why it looks like a Morning-shift problem (and isn't)

The helpdesk charges a breach to whoever *resolves* the ticket. Overnight tickets are picked up and closed by the Morning shift,
so Morning gets charged. Over the last 12 weeks, of the 452 breaches charged to Morning, 369 (82%) were created overnight. Only
83 happened on Morning's own watch. So the chat team Priya is worried about are right:
they open the day to a wall of red and can't do anything about it.

## Answers to the questions in the thread

- **Which agents?** I tested all 41 active agents on their own on-shift tickets over the last 8 weeks. **None** is statistically
  worse than the desk average. A typical agent resolves about 3 tickets a week, so any one week is noise; I would not use the
  weekly agent table to have a performance conversation. It is in the pack if you want it. It shows breaches from the overnight gap
  separately from breaches on the agent's own shift.
- **Arjun's credit line.** It has more than tripled: about Rs 0.36 lakh in Q2 2025, about Rs 1.9 lakh a quarter now. It went up in
  one step in July 2025, then stayed flat, which is why it looks "flat month on month" to Priya. The step is the roster change.
- **The June reshuffle "was cost-neutral".** It was cost-neutral on payroll; on credits it wasn't. About Rs 1.1 lakh a quarter of credits
  come from the overnight gap alone.
- **CSAT.** Breached tickets average 2.8 out of 5; the rest 3.5. That is the CSAT movement Priya saw.

## The number and the ask

**Cut the first-response breach rate from 25% to about 10%, worth about Rs 1.1 lakh a quarter in credits** on the tickets in your
export (about 172 a week). If your real volume is nearer the 650 a week I've heard, it scales to roughly Rs 4.3 lakh a quarter.

Headcount is frozen, so this has to be a move, not a hire: **put one agent back on the Night shift covering chat, social
and email.** Overnight volume in the export is about 5 tickets a night (roughly 20 at 650 a week). Two of the people moved off
Night last June, Tarun Mishra and Harpreet Deshpande (Indore), are the obvious candidates. Day-shift chat carried the same breach rate
(8%) when volume doubled, so it looks able to spare one person, but please check that against your own view of the floor.
A *new* night agent at Rs 165/hour x 8 hours would cost about Rs 1.2 lakh a quarter, roughly what it saves at export volume. So don't hire one.

## How far to trust this

I re-derived every breach, shift and cause for all 11,200 tickets with a second, independent piece of code and got zero
disagreements. Out of sample, the "no cover at creation" rule correctly calls 88% of tickets on the last three quarters, and misses
the ordinary 9% floor and the overnight emails. Things I could not check: the export has only the *resolving* agent, not who sent
the first reply; cover is judged from the roster, not from who actually turned up; and the export volume (172 a week) doesn't match
the 650 a week quoted. If the roster is out of date (for example an informal night rota), the finding weakens. Please confirm with
Sameer or the team leads that nobody was covering nights unofficially.

*I'd suggest not sharing the agent-level table with the Morning team as a league table. If you want one thing to say to them: the numbers show it isn't them.*
