# 3-minute walkthrough script (about 430 words at a relaxed pace)

**0:00 Show `out/report.html`, top box.**
"Neha asked for a breach report by agent and shift. I built it, and the first thing it shows is that agent and shift is the wrong
cut. Seventy-one percent of breaches are tickets created between ten at night and six in the morning, after the June 2025 roster
change left nobody on nights. Staffed hours breach at a flat nine percent."

**0:30 Terminal: `python -m vireo_sla`, then `python -m tests.validate`.**
"It runs from the README in about two seconds, no API keys. Validation re-derives every ticket's breach, shift and cause with a
separate row-by-row implementation. Eleven thousand two hundred tickets, zero mismatches."

**0:50 PROMPTS.md, versions.**
"The prompt I gave Claude Code was: build this end to end from the pack. Version one did exactly what she asked, breaches by
resolving agent. Morning had eighty-five percent and ten agents looked terrible. I threw that away as the headline, because the policy
says breaches are charged to the resolver and the night queue is picked up by the next shift. Version two split by creation shift and
found chat at a hundred percent overnight from the thirtieth of June."

**1:25 DECISIONS.md, row 7.**
"Version three used the ticket's assigned team to define an uncovered hour. That was wrong: it flagged pre-June Billing tickets that
were answered fine. I changed it to the channel's frontline team, which matches the data. Version four fixed the roster boundary: a one
a.m. ticket belongs to the previous night's shift."

**1:50 Report section 4, agents.**
"For agents, a typical person resolves three tickets a week, so weekly rankings are noise. The tool flags only on a rolling eight
weeks with an exact binomial test. Result: zero of forty-one flagged. I say that instead of inventing a list."

**2:10 What I threw away.**
"I dropped the resolver league table, the assigned-team rule, an IVR-failure flag that found ten rows not forty, and an LLM-written
summary I couldn't test and didn't need. The tool uses no paid model calls."

**2:30 MEMO.md, the number.**
"The goal: cut the breach rate from twenty-five to about ten percent, worth about one point one lakh rupees a quarter at the
export's volume, about four point three lakh if the real volume is six-fifty a week. The fix is one agent moved back to nights,
because headcount is frozen."

**2:50 SUBMISSION.md, question 5.**
"What's wrong with it: only the resolving agent is in the data, coverage comes from the roster not attendance, and the volume
doesn't match what Vireo told us."
