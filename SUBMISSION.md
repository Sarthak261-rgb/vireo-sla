# Submission: Vireo Audio Support Tickets (Set D)

Lines marked **[YOU]** are facts only the candidate can supply. Everything else is measured from this repo.

## 1. What did you build, and what business outcome does it move?

A small Python tool (`python -m vireo_sla`, pandas only) that turns the helpdesk export and roster into Neha's weekly breach
report by agent and shift, and splits every breach into *coverage gap* (ticket created while nobody from the channel's frontline
team was rostered) versus *in-shift*. The split is the point: 71% of breaches (1,579 of 2,229 in Jul 2025-Jun 2026) are
overnight tickets after the June 2025 roster change; staffed hours breach at a flat 9.4%.

**Goal: cut the first-response breach rate from 25% (24.9% over the last four quarters) to about 10% (9.6%), worth about Rs 1.1 lakh a quarter**
(Rs 114,220: 1,375 avoidable breaches a year x Rs 350 x share resolved, / 4) on the export's ~172 tickets a week.
If real volume is ~650/week, about Rs 4.3 lakh a quarter. Mechanism: move one existing agent back to Night (headcount frozen).
Secondary: breached tickets score 2.79 CSAT vs 3.53.

## 2. What does one run cost, and what would a month cost at ~650 tickets a week?

**No paid calls.** One run took 1.5 seconds wall-clock on 11,816 rows (measured): Rs 0 marginal. A month at 650 tickets/week
(650 x 52 / 12 = 2,817 tickets) is also Rs 0 in API cost, and time grows roughly linearly with rows.
For comparison, if someone added an LLM step that read each ticket's text (not built): assume ~600 input + 50 output tokens per ticket,
so 2,817 x 600 = 1.7M input and 0.14M output tokens a month. At Claude Haiku 4.5 list prices I recall as $1 / $5 per million tokens
(please verify), that is about $2.4, roughly Rs 200 a month. Cheap, but it adds nothing to the breach numbers, so I didn't build it.
Building cost: Claude Code on a subscription, no API spend I can see. I don't have a token-level cost for the session.

## 3. How do you know it works?

- **Implementation check.** A separate row-by-row implementation (stdlib csv/datetime, written from the policy text) re-derived breach,
  created shift, cause and resolver shift for **all 11,200 tickets: 0 mismatches**. Also 6 unit tests on boundaries (15:00 vs 15:01 minutes,
  22:00 IST, the 29/30 June roster move, dedupe, credit only on resolution).
- **Interpretation check (hold-out).** Rule learned on 2025-Q3 only, scored on 7,093 later tickets: accuracy 88.0%, precision 78.3%,
  recall 71.1%. **506 of 1,750 breaches (28.9%) are not explained by the rule.**
- **Placebo/consistency.** In-shift breach rate by quarter: 9.7, 8.9, 10.0, 9.2, 9.2, 9.2%. Before July 2025 there are 2 gap tickets, both on the night of 30 June.
- **The kind of case it gets wrong:** overnight *email* (49% breach; the rule says "no breach") because it depends on the exact hour: 91%
  breach at 22:xx, 59% at 23:xx, ~0% after 01:00. And in-shift breaches, which are a ~9% noise floor the tool doesn't try to explain.
- 30 random tickets with every derived field are in `out/validation_sample.csv` for anyone to eyeball. I did not hand-check them against the helpdesk UI (no access).
- Not verified: no ground-truth labels of "why did this breach", no first-responder id, no attendance data.

## 4. Did you change, narrow, or push back on the client's ask?

Yes. When: after the first cut (v1) gave the requested output and it contradicted the roster. What: (a) I led with shift/coverage cause rather than the
requested agent ranking; (b) I kept the weekly agent table but flag only on a rolling 8-week significance test, never Tier 2, and the result is
0 of 41 flagged; (c) I put both the helpdesk view and the cause view side by side, because Neha's "Morning team is the bulk of breaches" is true by count and wrong by cause;
(d) I said "don't hire", which Arjun already required, and gave a reassignment instead. Why: the report is meant to prepare a conversation with "the right people",
and the data says the right person is whoever owns the night roster. Priya also asked not to build something that makes the Morning team feel worse.

## 5. What is wrong with what you are handing us?

- Only the **resolving** agent is in the export. "In-shift" agent rates therefore use the resolver, not the person who replied first.
- Coverage comes from the **roster**, not attendance or leave. An informal night rota would make the finding weaker.
- The headline counterfactual assumes gap tickets would breach at the in-shift rate; it ignores the extra load on the person moved to Night.
- **Volume mismatch:** export ~172 tickets/week vs ~650 quoted. I don't know which is right; the scaled Rs 4.3 lakh is a linear extrapolation.
- Overnight email has an hour effect the tool doesn't model (only visible in the validation notes).
- The email thread PDF I was given ends on 9 Sep 2026 and showed "1/2" on its footer; I may have missed a second page. Also the README/thread PDFs were image-only; I read them visually.
- 1-week agent rows have tiny n (median 3); use the rolling table.
- Only ran on one export; no tests with malformed input (blank timestamps, unknown agent ids beyond dropping/failing).
- Timezone rule rests on one check (voice hours). Legacy rows might differ; I saw no evidence, but no other check exists.
- Report is basic HTML with no charts.
- Clean-machine check: I cloned the repo to a temp folder and ran the README steps with system Python (report, 6 tests and validation all pass). A fresh `venv` + `pip install pandas` on this Windows box was blocked by an Application Control policy (DLL load failure), so the pip step itself is untested here.
- Shift-per-roster-row lookup assumes one active roster row per agent per day; there is no explicit check.

## 6. What did you deliberately leave out, and why that rather than something else?

Refund/replacement analysis, product/lot defect clustering (Pulse 2 launch, lot codes), category re-tagging, repeat-contact costing, transfers (Rs 305 each),
Tier 2 resolution-days, and any LLM use. I left them out because the client asked for SLA breaches and the breach data alone explained 71% of them; each of the others would
have been a second project and none would have made the breach conclusion more trustworthy. I picked validation over breadth: a wrong causal claim in front of a Finance Controller is worse than a missing chart.

## 7. Anything you built or found that nobody asked for?

- **The cause of the credit tripling** (Arjun): a step change in July 2025 from the roster move, then flat. It also reconciles Priya's "credits look flat month on month".
- The "naive vs correct" comparison: reading UTC as IST puts 68% of tickets in the wrong shift; not deduping inflates breaches by 115.
- 6 tickets with both refund and replacement (policy s5 says escalate the same day; Rs 13,945 of refunds), found in passing, not investigated.
- A rolling significance test for agents.

## 8. What did you use AI for?

Claude Code (Claude Sonnet 5.5) for reading the PDFs, exploring the data, writing all code, tests and docs. It helped most on exploration speed and finding the
overnight pattern; it wasted time on the `assigned_team` coverage rule (v3, wrong) and a bash heredoc that silently failed. Thrown away: resolver league table, assigned_team rule,
IVR-length flag, an LLM narrative step (see PROMPTS.md). Runtime tool uses no AI. Walkthrough video: `video/vireo_walkthrough.mp4` (2:17). **Disclosure: it is built from screenshots of the real outputs with text-to-speech narration (`VIDEO_SCRIPT.md`), not a live screen recording of me. [YOU: re-record over the same script in your own voice if you want, and add the hosted link.]**

## 9. Someone picks this up on Monday and you are unreachable. The three things they need to know.

1. Confirm with the team leads that nobody informally covers 22:00-06:00 chat/email. The whole finding rests on the roster being true. If nights are covered, the finding is wrong.
2. Ask Sameer for the first-responder agent id (and the real weekly volume). That removes the two biggest limits.
3. Don't circulate the agent table as a league table: use `out/agent_flags.csv` (rolling, tested); `weekly_by_agent.csv` is a reference file. Rerun with `python -m vireo_sla` after each weekly export.

## 10. Honest hours spent

**[YOU: one number.]** The AI-assisted build itself ran in one continuous session; the number is yours to state.

## 11. GitHub repo link

**[YOU: link]**. Repo folder: `vireo-sla/`.
