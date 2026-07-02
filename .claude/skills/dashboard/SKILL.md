---
name: dashboard
description: Build or update the JAX HVAC dashboard artifact. Use when Zaal asks for the dashboard, to update it, or after a dat-review or valve-sweep produces new data. Renders DAT status, valve load, alarms, MaintainX WOs, and the field checklist as a claude.ai artifact.
---

# JAX HVAC Dashboard

A single self-contained HTML artifact (dark theme) that Zaal reads on his phone
between mechanical rooms.

## Data sources (all in-repo)

- `hvac/data/snapshots/dat_*.json` — latest DAT snapshot (+ previous for trends)
- `hvac/data/snapshots/valves_*.json` — latest valve sweep + analysis
- `hvac/data/maintainx_snapshot.json` — open WOs (if pulled)
- `hvac/data/journal/<date>.jsonl` — field notes / checklist material
- `hvac/data/metasys_points.json` — labels, bands, topology quirks, CHW sources

## Sections (keep this order)

1. Header with date + ACTION NEEDED badge (red if any critical)
2. KPI tiles (critical/high/low/fault/override/ok) — click to filter
3. Building grid — worst-status color per building, click to filter
4. Priority units table — delta bars, AM→PM trend arrows, action notes
5. Cooling valve load — callout (plant analysis), tier filter chips
   (default: "Problem — 100% & DAT >57°F"), distribution bars, table
6. Overrides & faults
7. Collapsible all-units table
8. Overnight alarms
9. MaintainX WOs (with JSON import box)
10. Tomorrow checklist (localStorage persistence)

## Rules

- Read the `dataviz` skill before styling new chart types.
- Self-contained: no external requests (artifact CSP blocks them). Inline everything.
- Mobile first: tables wrapped in `overflow-x:auto`; page never scrolls sideways.
- Status colors are reserved (critical red #d03b3b, high #ec835a, warn #eda100,
  low blue #3987e5, ok green #0ca30c) and never reused for identity.
- No horizontal-rule dividers. Short labels. Tabular numerals in tables.
- Keep the SAME artifact file path across updates (`hvac_dashboard.html` in the
  scratchpad) so it redeploys to the same URL; keep favicon 🌡️ stable.
- Syntax-check the inline JS with `node -e "new (require('vm').Script)(...)"`
  before every redeploy.
- Known quirks to reflect in notes: B12 AS-4 decommissioned; F&B 1/3-2/3 valves
  at 100% are normal; position feedback often unwired; B55+B50 share CHW pumps.
