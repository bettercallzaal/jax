---
name: work-order
description: Draft a MaintainX work order with the JAX-required fields, or pull/triage open WOs. Use when Zaal asks to make a WO, draft a work order, or review open MaintainX work orders. Fills GL account, Maximo worktype/status, category, and links WOs to affected AHUs.
---

# MaintainX Work Orders

## Creating a WO

Two paths, pick based on whether MAINTAINX_API_TOKEN is set and whether the JAX
custom fields matter for this WO:

- **API create** (`hvac maintainx-create` / `create_work_order` tool) — creates the
  WO directly in MaintainX. Only sets standard fields: title, description, priority,
  due date. It does **not** set GL Account, MAXIMO WORKTYPE/STATUS, or Category — that
  custom-field mapping hasn't been confirmed against the live API yet (MaintainX's docs
  site blocks automated fetches; needs either a pasted docs excerpt or a live-token
  test to nail down). After an API create, still open the WO in MaintainX and fill
  those fields in by hand before assigning it out.
- **Draft-and-hand-off** — still the right path when you want every required field
  filled at creation time, or when there's no token configured. Produce a clean,
  paste-ready draft and hand it to Amy Briggs (the coordinator) or enter it yourself.

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

Use `hvac.agent`'s `draft_work_order` tool for the paste-ready draft, or
`create_work_order` / `hvac maintainx-create` for the API path above.

## Pulling / triaging open WOs

- Live pull: `hvac maintainx-pull` (needs `MAINTAINX_API_TOKEN`) writes
  `hvac/data/maintainx_snapshot.json`. The client is cursor-paginated with 429 backoff.
- No token yet? Zaal pastes the Work Orders list; parse it into the same snapshot shape.
- Triage: surface BAS/HVAC + open/overdue first; drop the campus noise.
- **Link WOs to units on the dashboard** — match room/building to AHUs:
  e.g. 55-2504B/2504D + "55-2504 suite very hot" → B55 AHU-3 (the strainer job);
  "CWP-15 impeller" → the CHW plant callout; "B56 AHU-1 Broken OA Damper" → B56 units.
- Status updates (OPEN/IN_PROGRESS/ON_HOLD/DONE) can be pushed via
  `update_work_order_status` in `hvac/briefing/maintainx.py` — same token, no coordinator
  hand-off needed for a status change.
- Comments and attachments are **not** wired up yet — the API supports both but the
  exact endpoint shape wasn't confirmed (docs site blocked automated fetches). Don't
  build on `add_comment`/`add_attachment` until that's verified against a real token.

## Style

Short, direct, no dividers. When drafting, output the paste-ready block and nothing
else the user has to edit around.
