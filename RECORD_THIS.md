# Record this (one voice recording, about 2:45 at a normal pace)

**How to record**
- Use your phone's voice recorder. Quiet room. Speak at a normal pace. The limit is 3:00, so don't add extra lines.
- Read the 8 parts below in order, as ONE recording.
- **Between parts, stay silent for 3 seconds.** That gap is how the recording is split so each part lines up with the right screen.
- If you make a mistake, pause 3 seconds and re-read that part from the start. Tell me which parts you repeated.
- Don't read the part numbers or the words in brackets out loud.

---

**Part 1** (report top)
Neha asked for a breach report by agent and by shift, so she can talk to the right people. I built that. But the data shows that agent and shift is the wrong way to look at it. Seventy-one percent of all breaches are tickets that arrive between ten at night and six in the morning. Since June 2025, nobody has been rostered on chat or email at night. Outside that gap, when someone is on shift, tickets breach at a flat nine percent, in every quarter.

*(3 seconds silence)*

**Part 2** (terminal)
The tool runs from the README in about two seconds. It needs no API keys, and it makes no paid calls. To check it, I wrote a second, separate version of the logic, row by row, and compared the two on all eleven thousand two hundred tickets. There were zero differences. I also have unit tests for the edge cases, like a reply at exactly fifteen minutes.

*(3 seconds silence)*

**Part 3** (prompts and versions)
I used Claude Code to build this. My prompt was: build this end to end from the pack. Version one did exactly what Neha asked, breaches by the agent who resolved the ticket. It made the Morning shift look terrible, with eighty-five percent of breaches. I threw that away as the headline. The policy says the night queue is picked up by the morning shift, so Morning was being blamed for tickets that arrived while nobody was on. Version two looked at when the ticket was created, and found that every overnight chat breaches, from the thirtieth of June 2025.

*(3 seconds silence)*

**Part 4** (decisions)
Version three was wrong. I used the ticket's assigned team to decide who was on cover, and that flagged tickets that were actually answered fine. I changed it to use the channel's own front-line team, and that matched the data. Version four fixed a boundary bug: a ticket at one in the morning belongs to the previous night's shift. I also converted all times from UTC to Indian time, because otherwise most tickets land in the wrong shift.

*(3 seconds silence)*

**Part 5** (agents table)
For agents, a typical person resolves only about three tickets a week, so a weekly ranking is just noise. So the tool only flags someone if they are clearly worse than average over eight weeks, using a statistical test. Escalations and Warranty are never flagged, because the policy says they can't be compared on volume. The result is zero of forty-one agents flagged. I report that honestly, instead of inventing a list.

*(3 seconds silence)*

**Part 6** (thrown away)
Here is what I threw away: the agent league table, because it is mostly noise and it would demoralise people. The assigned-team rule. A flag for failed phone transcripts that found ten rows instead of forty. And an AI-written weekly summary, which I could not test and did not need. The final tool makes no AI calls.

*(3 seconds silence)*

**Part 7** (memo, the number)
The goal is to cut the breach rate from twenty-five percent to about ten percent. That is worth about one lakh ten thousand rupees a quarter in credits at the export's volume, and about four lakh thirty thousand if real volume is six hundred fifty tickets a week. Headcount is frozen, so the fix is to move one existing agent back to the night shift. Overnight volume is only about five tickets a night.

*(3 seconds silence)*

**Part 8** (what is wrong)
What is wrong with it: the data only has the agent who resolved the ticket, not who replied first. Coverage comes from the roster, not from who actually turned up. The export has about a hundred and seventy tickets a week, but Vireo says six hundred fifty, and I could not resolve that. The full list is in the submission.
