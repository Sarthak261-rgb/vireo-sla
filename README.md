# Vireo Audio: first-response SLA breach report

Weekly breach report by agent and by shift, built for Neha Kulkarni (Support Ops). It also answers a question
she did not ask: *why* the breaches happen. In one line: **71% of breaches are tickets created overnight
(22:00-06:00 IST) after the June 2025 roster change left no chat/email night staff. Staffed hours breach at a flat 9%.**

No API keys, no network, no paid calls. Python 3.10+ and pandas only.

## Run it (clean machine)

```bash
git clone <this repo> && cd vireo-sla
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# put the client export in ./data/ with these names (the raw files carry a UUID prefix - strip it):
#   data/tickets.csv   data/agents.csv     (orders/customers/products are not needed by the report)
python -m vireo_sla                     # writes out/report.html + CSVs, prints a 2-line summary (~2 s)
python -m vireo_sla --week 2026-06-01   # report as of another week (give the Monday)
python -m unittest tests.test_units     # 6 unit tests, no data needed
python -m tests.validate                # independent re-implementation on all tickets + hold-out; writes out/validation.md
```

`data/` is git-ignored (client data). `out/` is committed so the result can be read without running anything:
open `out/report.html`.

## What it does

1. **Cleans** the export: drops the 616 tickets duplicated by the Freshdesk migration (keeps the helpdesk copy),
   converts UTC to IST before assigning shifts and weeks, treats CSAT 0 and blank as "no response", and counts a breach as
   first response *strictly later* than the policy target (chat 15 min, voice 2 h, social 4 h, email 8 h).
2. **Attributes each breach to a cause**: `coverage gap` (nobody from the channel's frontline team was rostered on
   the shift the ticket was created in, using the effective-dated roster) or `in-shift`.
3. **Reports weekly by shift and by agent**, with the helpdesk's view (breach charged to the resolving agent) beside the
   cause view. An agent is flagged only if statistically above the desk's on-shift rate
   (>=30 on-shift tickets in 8 rolling weeks, one-sided exact binomial p<0.01; Tier 2 is never flagged).
4. **Puts a rupee number on it** (`out/headline.json`): avoidable credits per quarter if gap tickets breached at the
   in-shift rate.

## Files

| Path | What |
|---|---|
| `vireo_sla/clean.py` | load, dedupe, UTC->IST, targets, credits |
| `vireo_sla/attribute.py` | roster join, coverage-gap logic |
| `vireo_sla/metrics.py` | weekly tables, agent flag rule, headline numbers |
| `vireo_sla/report.py` | CSV + HTML output |
| `tests/test_units.py` | edge cases: 15-minute boundary, 22:00 IST, roster move on 30 Jun, dedupe, credit on resolution |
| `tests/validate.py` | independent row-by-row re-implementation, hold-out test, "naive report" comparison |
| `DECISIONS.md` | every judgement call and why |
| `MEMO.md` | one-page memo to Neha |
| `SUBMISSION.md` | answers to the 11 submission questions |
| `PROMPTS.md` | prompts, versions, what was thrown away |
| `VIDEO_SCRIPT.md` | narration for the 3-minute walkthrough |
| `out/` | generated report, CSVs, validation results |

## Known limits (details in SUBMISSION.md)

The export only has the *resolving* agent, not who sent the first reply. Coverage is judged from the roster, not from
actual attendance. The export holds about 170 tickets a week while Vireo says about 650; this is unresolved.
