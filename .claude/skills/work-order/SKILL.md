---
name: work-order
description: Draft a MaintainX work order with the JAX-required fields, or pull/triage open WOs. Use when Zaal asks to make a WO, draft a work order, or review open MaintainX work orders. Fills GL account, Maximo worktype/status, category, and links WOs to affected AHUs.
---

# MaintainX Work Orders

## Drafting a WO

Zaal can't create WOs via API on the fly here — Amy Briggs is the coordinator who
creates them. So produce a clean, paste-ready draft with every REQUIRED field filled,
so he can hand it to Amy or enter it himself.

Required fields on the JAX MaintainX form (confirmed from live WOs):
- **Title** — short, location-first (e.g. "B55-2504D check/adjust temps")
- **Description** — symptom + what's been checked + any WO lineage
- **Location** — building/room, e.g. `55-2504D`
- **Priority** — High / Medium / Low
- **Work Type** — Reactive (for complaints/faults)
- **MAXIMO WORKTYPE** — CM (corrective maintenance)
- **MAXIMO STATUS** — APPR
- **GL ACCOUNT** — `6026200-RLAB` for RLAB-end BAS work. NOTE: first digits vary by
  campus end, suffix by work type/area — confirm the exact code with Amy per job.
- **Category** — BAS (for controls/HVAC)
- **Assign to** — Zaal Panthaki

Use `hvac.agent`'s `draft_work_order` tool, or produce the same block directly.

## Pulling / triaging open WOs

- Live pull: `hvac maintainx-pull` (needs `MAINTAINX_API_TOKEN`) writes
  `hvac/data/maintainx_snapshot.json`. The client is cursor-paginated with 429 backoff.
- No token yet? Zaal pastes the Work Orders list; parse it into the same snapshot shape.
- Triage: surface BAS/HVAC + open/overdue first; drop the campus noise.
- **Link WOs to units on the dashboard** — match room/building to AHUs:
  e.g. 55-2504B/2504D + "55-2504 suite very hot" → B55 AHU-3 (the strainer job);
  "CWP-15 impeller" → the CHW plant callout; "B56 AHU-1 Broken OA Damper" → B56 units.

## Style

Short, direct, no dividers. When drafting, output the paste-ready block and nothing
else the user has to edit around.
