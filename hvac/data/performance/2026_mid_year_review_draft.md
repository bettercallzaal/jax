# 2026 Mid-Year Review — Zaal Panthaki, BAS Technician

Manager: Wayne Cameron
Period: 01/01/2026 – 07/08/2026

## Goal-by-Goal Status

**2026 Annual Calibrations** — In Progress. On pace; confined-space units still depend on attendant (James) scheduling for Q3.

**2026 Training & Development (JCI training, best practices)** — In Progress. Concrete progress beyond the formal training itself: independently traced a JCI FEC's block-level program (ZN-T Setpoint Determination, Autocalibration Sequence, Remote Setpoint Mode) to find and fix a root cause in Rm 1530 — see Big Wins.

**Departmental Goals 2026 (Safety/MaintainX/Machine Spaces/Communications)** — In Progress. Zero injuries/near-misses maintained; WO documentation discipline continued from 2025.

**Gainesville Weekly Alarm Audits** — Ongoing, on schedule.

**Maintenance Capital Projects 2026** — In Progress/supporting as needed (B28 Air Compressor, Autoclave, JCI Upgrades, RAF VSDs, B57 RTU, CRAC replacement, and others).

**AHU Documentation Refresh (carryover, due 03/31/2026)** — status needs confirming against the 100% target.

## Big Wins (H1 2026)

- **53-1416 warm-room complaint (WO #400074)** — full end-to-end resolution over two days: replaced a faulty network controller, corrected reheat wiring, replaced a leaking radiation valve, then diagnosed an apparently "reverse-acting" JCI VA-7452-90011 actuator down to a disconnected common wire (not a jumper/config issue as it first appeared) — root-caused rather than swapped parts until something worked.
- **Campus DAT crisis response (7/1–7/6)** — triaged 60+ AHUs across repeated daily sweeps, correctly separated unit-level faults from a plant-level root cause (B17/NAE-20 secondary chilled-water capacity) driving the whole B28 cluster instead of chasing it AHU by AHU, tracked a same-day relapse back to its cause, and drove the campus from 9 critical/17 high down to 1 critical/3 high.
- **B55 AHU-3 strainer diagnosis** — recognized that a 19.8°F CHW delta-T looked healthy but was actually a low-flow signature, not proof of a good coil; avoided closing the ticket on a false read.
- **B6 AHU-1** — caught and corrected my own earlier theory (OAT sensor lockout) mid-investigation by cross-referencing a compressor alarm timestamp against the DAT timeline, and found the real cause (a cycling compressor) within the same day.
- **B01e Rm 1530 "Breezeway Office" (WO #400161)** — first pass found a +2°F sensor offset and zero cooling modulation range (CLG-MAXFLOW pinned equal to CLG-MINFLOW); follow-up dive traced the actual JCI controller logic end-to-end and found a stale network-priority setpoint silently overriding the physical thermostat the whole time — fixed the setpoint routing and the airflow cap, then verified live by physically changing the thermostat and watching the controller respond correctly for the first time.
- **Sterile Storage Room Pressure alarm** — used trend correlation (supply flow vs. exhaust flow vs. damper command vs. room pressure) to rule out a supply-side or control-loop fault before concluding the cause was environmental (active nearby construction) rather than chasing equipment that wasn't broken.
- **Weekend AC scheduling request (B01e-3250)** — identified that the request conflicted with the energy-savings policy and escalated for direction instead of just making the change.
- **HVAC BAS Field Toolkit** — not a one-time project: continued extending it this year (MaintainX work-order integration, structured field journal, dashboard) as new needs came up, and it's now in daily use for triage and documentation.

## How I Grew

- **CCT/JCI programming depth** (last year's named growth area): went from treating BAS setpoints as values to adjust, to actually tracing a JCI FEC's block-level program — setpoint determination logic, autocalibration state machine, remote setpoint routing — to find a root cause that wasn't visible from the summary screen at all.
- **Systems thinking over unit-level fixes**: repeatedly stepped back from "is this one unit broken" to "is this the plant" (B28/NAE-20 secondary CHW) and from "did this fix work" to "what's the actual mechanism" (Sterile Storage trend analysis) instead of chasing symptoms one AHU at a time.
- **Verification discipline**: consistently re-checked fixes against real data (delta-T, temp-gun readings, trend history) before closing tickets, and more than once caught that an apparent fix hadn't actually held or was coincidental.
- **Independent diagnosis on ambiguous problems**: increasingly working cases with no obvious first move — deciding what to check and in what order before touching equipment — directly the "faster field diagnosis" item from last review.
- **End-to-end ownership**: coordinated with Bob on legacy N2/CCT programming access, worked the parts/procurement side with vendors, and escalated a policy conflict rather than resolving it unilaterally.

## Challenges

- Write access on legacy N2-trunk devices is inconsistent — some points can be overridden directly, others still require looping in Bob's tooling, which slows down programming-depth work.
- Confined-space calibration attendant coverage (James) remains a scheduling dependency for remaining Q3 units.
- Position feedback is frequently unwired campus-wide, which creates diagnostic blind spots that have to be worked around case by case rather than trusted at face value.

## Next-Half Targets

- Finish 2026 Annual Calibrations and close out the AHU Documentation Refresh carryover.
- Continue building CCT/JCI programming depth through formal JCI training, building on this year's self-taught block-tracing work.
- Confirm on-call rotation status against the 05/01/2026 target from last review.
- Keep extending the field toolkit as new diagnostic needs come up.
