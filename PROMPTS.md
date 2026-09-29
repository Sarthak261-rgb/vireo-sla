# Prompts, versions, and what was thrown away

Built with Claude Code (Claude Sonnet 5.5) doing the analysis and code. The tool itself calls no model API.

## The prompt I gave (trimmed)
> "this u need to develop and here are the documents ... make this and build this from end to end and record a video urself if possible and i need everything ready here"

plus the brief, the pack files, and the 11 submission questions.

## Versions
- **v0, read the pack.** The README and email thread are image-only PDFs (text extraction came back empty), so I rendered them to
  PNG and read them. The policy PDF held the traps: breach is charged to the *resolving* agent; the night queue is picked up by the
  next shift; the export is UTC; migration duplicates; CSAT 0; roster rows with dates.
- **v1, "do what she asked".** Breach by resolver agent and resolver shift, weekly. Result: Morning holds ~85% of breaches and ten
  agents sit at 30-50% breach rates. Clean story about the morning team, and wrong about cause. Not used as the headline.
- **v2, by creation shift.** Chat created 22:00-06:00 IST breaches 100% from 30 Jun 2025, 8% before. The roster shows the night
  chat/email agents were moved to Day (2 people) or left (3) on 29 Jun 2025. Morning's "wall of red" is their overnight inheritance.
- **v3, coverage via `assigned_team`.** Wrong: it flagged pre-June night tickets in Billing/Logistics as gaps although they were
  answered. Changed to channel -> frontline team (DECISIONS #7).
- **v4, boundary fixes.** The Night shift date rolls back before 06:00. Report as-of the last complete week. Exact binomial test for
  agent flags (no scipy dependency).
- **v5, validation.** Independent row-by-row reimplementation of four derived fields on all 11,200 tickets, plus a hold-out test.

## Thrown away
- Resolver-based weekly agent league table as the main output: demoralising, mostly noise, misattributes cause.
- The `assigned_team` coverage rule (v3).
- A "failed IVR transcript" flag by text length: only 10 rows under 25 characters, not the ~40 Sameer mentioned, and it does not affect timing.
- An optional LLM "weekly narrative" step. Not built: no API key in this environment to test it, and a numbers report should not be worded by something I cannot verify.
- Repeat-contact and CSAT-driver analysis. Breached tickets do have lower CSAT (2.79 vs 3.53), but a crude customer+SKU key showed no repeat-contact effect, so I built nothing on it.
