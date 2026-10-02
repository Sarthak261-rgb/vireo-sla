# Record this (one voice recording, about 2:45)

## Before you press record
- Phone voice recorder, quiet room, phone about a hand's width from your mouth.
- Do one practice read first. Aim for calm and clear, like explaining to a colleague. Don't perform it.
- Speak at a normal pace. Total limit is 3:00. This script is about 2:45, so don't add lines.
- Between parts, stay silent for **3 seconds** (count "one, two, three" in your head). That gap is how I split the recording to match the screens.
- If you slip, pause 3 seconds and re-read that part from its start. Tell me which parts you repeated.
- Don't read the part numbers, the bracketed screen names, or the *(pause)* notes.

---

**PART 1** [screen: report, yellow box]
Hi, I'm Sarthak. This is my submission for the Vireo Audio support tickets task.
Neha asked for a weekly report of which agents and which shifts breach the first-response SLA the most. I built that. But the data shows it's the wrong question. **Seventy-one percent of breaches are tickets that arrive between ten at night and six in the morning.** Since June 2025, nobody has been rostered on chat or email at night. When someone is on shift, tickets breach at a flat nine percent, in every quarter.

*(pause 3 seconds)*

**PART 2** [screen: terminal]
The tool runs from the README in about two seconds. No API keys, no paid calls.
To check it, I wrote a second, separate version of the logic and compared the two on all eleven thousand two hundred tickets. **Zero differences.** There are also unit tests for edge cases, like a reply at exactly fifteen minutes.

*(pause 3 seconds)*

**PART 3** [screen: prompts and versions]
I built this with Claude Code. My prompt was: build this end to end from the pack.
Version one did exactly what Neha asked, breaches by the agent who resolved the ticket. It made the Morning shift look terrible, with eighty-five percent of breaches. I threw that away as the headline. The policy says the morning shift picks up the night queue, so Morning was being blamed for tickets that arrived while nobody was on.
Version two looked at when each ticket was created. **Every overnight chat breaches, from the thirtieth of June 2025.**

*(pause 3 seconds)*

**PART 4** [screen: decisions]
Version three was wrong. I used the ticket's assigned team to decide who was on cover, and that flagged tickets that were actually answered fine. So I switched to the channel's own front-line team, and that matched the data.
Version four fixed a boundary bug. A ticket at one in the morning belongs to the previous night's shift. I also converted all timestamps from UTC to Indian time, because otherwise most tickets land in the wrong shift.

*(pause 3 seconds)*

**PART 5** [screen: agents table]
For agents, a typical person resolves only about three tickets a week, so a weekly ranking is mostly noise.
So the tool flags someone only if they're clearly worse than average over eight weeks, using a statistical test. Escalations and Warranty are never flagged, because the policy says they can't be compared on volume.
The result: **zero of forty-one agents flagged.** I report that honestly, instead of inventing a list.

*(pause 3 seconds)*

**PART 6** [screen: thrown away]
What I threw away: the agent league table, because it's mostly noise and it would demoralise people. The assigned-team rule. A flag for failed phone transcripts that found ten rows instead of forty. And an AI-written weekly summary, which I couldn't test and didn't need. The final tool makes no AI calls.

*(pause 3 seconds)*

**PART 7** [screen: memo, the number]
The goal: cut the breach rate from **twenty-five percent to about ten percent.** That's worth about one lakh ten thousand rupees a quarter in credits at the export's volume, and about four lakh thirty thousand if real volume is six hundred fifty tickets a week.
Headcount is frozen, so the fix is to move one existing agent back to the night shift. Overnight volume is only about five tickets a night.

*(pause 3 seconds)*

**PART 8** [screen: what's wrong]
Finally, what's wrong with it. The data only has the agent who resolved the ticket, not who replied first. Coverage comes from the roster, not from who actually turned up. And the export has about a hundred and seventy tickets a week, while Vireo says six hundred fifty. I couldn't resolve that.
The full list is in the submission. Thanks for watching.
