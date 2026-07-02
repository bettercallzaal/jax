---
name: dat-review
description: Run the daily campus DAT review from a pasted Metasys export. Use when Zaal pastes a Metasys discharge-air-temperature export or asks to review DATs / "how's it all look". Parses the paste, compares against the previous snapshot, flags critical/high/low units, writes a new snapshot, logs to the journal, and updates the dashboard.
---

# Daily DAT Review

Zaal (BAS Technician, The Jackson Laboratory) pastes a Metasys export of campus AHU
discharge air temperatures 1-2x per day. Turn it into a triaged review.

## Procedure

1. **Parse the paste.** Rows carry: unit label, DAT value, setpoint (or band).
   Unit labels and setpoint bands live in `hvac/data/metasys_points.json` — use it to
   resolve ambiguous labels and get `sp_low`/`sp_high`. Ignore units with
   `"active": false` (e.g. B12 AS-4 is decommissioned — its high reading is not actionable).

2. **Classify** with the toolkit thresholds (`hvac/briefing/dat_review.py`):
   critical = DAT >10°F above SP, high = 3-10°F above, low = >3°F below.
   Flag comm faults and operator overrides separately.

3. **Compare to the previous snapshot** in `hvac/data/snapshots/dat_*.json` —
   report per-unit trend (better/worse/new/resolved), not just today's state.

4. **Do the systems look before unit-level diagnosis** (this is mandatory — it's in
   the RAG chunks `dat-review-systematic` and `dat-review-campus-valve-sweep`):
   - Multiple units high in ONE building/engine → suspect OAT-sensor cooling lockout
     (locals stuck below the 52°F chiller-start SP). Known offenders: NAE-28, NAE-10, SNE-14.
   - Units pinned across MANY engines → check the shared CHW pump system.
     CHW topology is federated — see `chw_sources` in metasys_points.json
     (B55+B50 share pumps 3&4 in B50 B-101-A; B53 has its own pumps 1&2).
   - Face & bypass units (B53 AHU-1A/1B): 1/3+2/3 valves at 100% is NORMAL.

5. **Write the snapshot** to `hvac/data/snapshots/dat_<YYYY-MM-DD>T<HH>.json`
   (same shape as existing files: `taken_at`, `source`, `notes`, `units` list with
   `label/dat/sp_low/sp_high/flag`, plus prior reading as `am_dat` when comparing).

6. **Log findings** to the journal (`hvac.journal.log_observation`) and update the
   dashboard artifact if one is live this session.

7. **Report to Zaal**: worst units first, trends, which are systemic vs unit faults,
   and a prioritized go-look list. Short and direct — he's usually on his phone
   between mechanical rooms. Never use horizontal-rule dividers.

## Style

No fluff. Lead with the worst units and what to do about them. Include °F deltas.
Commit snapshot + journal to the repo when done.
