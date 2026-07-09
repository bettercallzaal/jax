---
name: troubleshoot
description: Guided, plain-language help diagnosing an HVAC/BAS comfort or equipment complaint step by step — pulls known campus quirks, journal history, and runs the decision-tree diagnostics, without requiring Metasys/CLI fluency. Built so Wayne (or anyone on the team without Zaal's day-to-day toolkit familiarity) can troubleshoot a complaint on his own. Use when someone describes a symptom like "room X is too hot/cold" or "AHU Y alarming" and wants help figuring out what's wrong and what to check next.
---

# Troubleshooting a Complaint

Wraps the same HVAC field toolkit Zaal built and uses daily, but as a guided
conversation instead of CLI commands — built for Wayne (or anyone without Zaal's
day-to-day Metasys/CLI fluency) to actually run a diagnosis end to end.

## Steps

1. **Get the basics in plain language.** Building/room or AHU tag, and the symptom
   (too hot, too cold, alarm, noise, whatever it is). Don't require Metasys jargon —
   translate as needed.

2. **Check for known quirks first.** Grep `hvac/data/metasys_points.json` for the
   building/zone — shared plants, decommissioned units, known-unreliable feedback
   points, prior sensor calibration issues. This is often the fastest way to rule out
   a known repeat issue before diagnosing from scratch.

3. **Check journal history for the same zone.** `python -m hvac.cli journal` shows
   today; grep `hvac/data/journal/*.jsonl` for the building/room to see if this is a
   new complaint or a relapse of something already worked. Say so plainly if it's a
   repeat — that changes the diagnosis.

4. **Pull relevant field knowledge directly** — Grep `hvac/data/rag_store.json` and
   `hvac/data/sequences/*.txt` for the building/system/symptom. You're already the
   LLM in this conversation, so read the knowledge base yourself rather than shelling
   out to `hvac.cli ask` (that command makes its own separate Claude API call — fine
   for a bare CLI session, redundant and an unnecessary API cost here).

5. **Ask only for what the next step actually needs** — not everything at once: zone
   temp, setpoint, discharge air temp, valve/damper output vs. feedback. If Wayne
   doesn't have a number, say exactly which Metasys screen/point to check (mirror the
   "what tab, what point, in what order" style from Zaal's own field process — don't
   make him guess where to look).

6. **Run the matching decision-tree diagnostic instead of guessing:**
   - Comfort complaint → `python -m hvac.cli diagnose-zone --zone "..." --room-temp X
     --setpoint Y [--discharge Z --cfm N --design-cfm N --co2 N --rh N]`
   - Reheat looks off → `python -m hvac.cli diagnose-reheat --zone "..." --discharge X
     --output Y [--hw-supply --hw-return --signal --type hot_water|electric]`
   - Full warm-room workup → `python -m hvac.cli analyze --zone "..." --discharge X
     --output Y [--room-temp --setpoint --cfm --mixed-air --hw-supply --hw-return]`

7. **Translate findings into 2-3 concrete next actions**, not a wall of diagnostic
   codes — "check X, then Y" beats a dump of raw Finding objects.

8. **Offer to log the outcome** —
   `python -m hvac.cli log --zone "..." --description "..." --tags "..."` — so it
   lands in the same shared journal Zaal already works from. One record, not two
   separate systems.

## Style

Plain language over BAS jargon — translate Metasys terms the first time they come
up. Short, direct answers: lead with what to check next, not a lecture on theory.
Same voice as the rest of this toolkit.

## Known quirks worth surfacing proactively

- B12 AS-4 is decommissioned — a reading here isn't meaningful, don't chase it.
- Position feedback is frequently unwired campus-wide — don't treat a flat feedback
  reading against a moving commanded output as proof of a stuck actuator on its own;
  note it and keep going.
- B55 and B50 share CHW pumps — a strainer/plant issue on one can show up on the
  other.
- F&B 1/3–2/3 valves sitting at 100% is normal, not a fault.
