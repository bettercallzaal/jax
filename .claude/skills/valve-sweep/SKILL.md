---
name: valve-sweep
description: Analyze a pasted Metasys campus cooling-valve export (the "bigger systems look"). Use when Zaal pastes a Cooling Valve Command/Position export or asks which valves are pinned. Tiers units into starved / at-max / unit-fault, checks plant-level patterns, writes a snapshot, and updates the dashboard.
---

# Campus Cooling-Valve Sweep

The plant-vs-unit diagnostic. Zaal pastes the campus "Cooling Valve" point export
from Metasys (all Cmd/Position/Output points, sorted by value).

## Procedure

1. **Parse rows** into: building, unit, cmd %, position % (may be absent), engine
   (from the Location/Reference path, e.g. JL-BLDG28-NAE28), and pair with the
   latest DAT snapshot in `hvac/data/snapshots/`.

2. **Exclusions before counting anything:**
   - `Minimum Cooling Valve Position` (CS Input Float) = setpoint floor, not a position.
   - Face & bypass units (B53 AHU-1A/1B and similar): 1/3+2/3 valves commanded 100%
     is normal sequence behavior.
   - Position feedback is often unwired at JAX — trust Command; flag cmd/pos
     mismatch >20 points as "check actuator/feedback", never as proof alone.
   - Object tree location ≠ physical building — resolve against `topology_quirks`
     in `hvac/data/metasys_points.json` (B12 on B51 SNE-03, B28 AHU-11 on B51,
     B53 AHU-3 on B55 SNE-01, etc.).

3. **Tier every unit** (rule of thumb from Zaal: pinned at 55°F is fine; pinned AND
   over 57°F is the problem):
   - STARVED: cmd ≥99% AND DAT >57°F — losing the fight.
   - AT MAX: cmd ≥99%, DAT holding SP — zero reserve, first to tip.
   - UNIT FAULT: DAT hot but valve mostly closed — actuator/control fault, NOT plant.

4. **Plant-level read:** count pinned valves per engine and per CHW system.
   CHW is federated (see `chw_sources` in metasys_points.json): B55+B50 share
   pumps 3&4 in B50 rm B-101-A; B53 has its own pumps 1&2. Many pinned on one
   system → check that system's pumps and suction strainers first. Wide CHW
   delta-T (~20°F vs 10-14 design) = LOW FLOW (clogged strainer / degraded pump).

5. **Write snapshot** to `hvac/data/snapshots/valves_<YYYY-MM-DD>T<HH>.json`
   (shape: `taken_at`, `source`, `analysis`, `valves` list), update the dashboard
   artifact, log notable changes to the journal, commit.

6. **Report**: the tier lists (starved first), what changed since last sweep, and
   the single most likely root cause with the next physical check.
