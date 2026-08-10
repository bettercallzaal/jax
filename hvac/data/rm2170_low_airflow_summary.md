# Room 2170 Low-Airflow Investigation — Summary (2026-08-10)

Building 1, Unit 4, Level 2 — open-office bullpen (~8 desks), flanked by Rooms 2185/2187.
Metasys point tree: "JacksonLabs" / controller `04B038FEC`.
Prepared for in-person discussion with Wayne. Full raw entries logged in `hvac/data/journal/2026-08-10.jsonl`.

## The complaint

Zone temp 71.5°F, above cooling setpoint 70.6°F — zone is actively calling for cooling and not getting it.

## What we confirmed by hand

- **Supply Air Damper**: commanded 100%, and visually confirmed at true full-open at the blade.
- **Actuator**: found a mis-clamped Johnson Controls M9208-GGA-3 with a 30% dead-zone offset; recalibrated it. Damper position now genuinely tracks command. This did **not** fix the airflow problem — a real but secondary fault.
- **Supply Flow**: tops out ~400 cfm against an 805 cfm setpoint, no matter how far the damper opens. Flow-vs-command curve shows hard diminishing returns: 30%→300 cfm, 55%→369 cfm, 70%→385 cfm.
- **Dry Pressure transmitter (Veris)**: reads 0.1 in.wc at the box even at full-open — genuinely low velocity, consistent with a real restriction, not a sensor fault.
- **Duct size**: measured ~10" round near the box. At 805 cfm that's ~1,476 fpm — a normal, correctly-sized design velocity. **This rules out "the duct was simply never sized for this much air"** as a blanket explanation — at least at the point measured.

**Conclusion so far**: this is a real physical restriction or upstream capacity limit, not a controls/actuator problem. Working theory has narrowed to: a localized restriction somewhere along the run (kink, crushed section, or a partially-closed manual volume damper/VD) — since the pipe itself is properly sized — or an AHU-wide static-pressure/capacity limitation. Not yet distinguished between these two.

## What we found in the drawings (Z:\Duct Prints, Z:\Administrative\Building Maps) — and where it got inconclusive

- **Architectural**: `01d-2.PDF` (Building Maps index) confirms Room 2170 is real, on Building 1 - Unit 4, Level 2, in the office/cubicle cluster 2075–2187 (drawing dated 2019.04.09).
- **AHU-10 ruled out**: no "B1 AHU-10" object exists anywhere in `hvac/data/metasys_points.json` — only a B21 AHU-10 (different building). Colleague's guess doesn't check out.
- **AHU-14 candidate**: `Z:\Duct Prints\B01 D\Feed From AHU14\MH101.pdf` (1st floor) and `MH102.pdf` (2nd floor) — WBRC Project 2882.38, "AS BUILT 11-28-03," literally titled "Jackson Laboratory Unit 4 Renovation." Room 2170 is labeled by name on MH102, on the same sheet as VAV-12 (Rm 2090) and VAV-13 (Rms 2085A/2085B). Metasys object numbering also lines up: Room 2170's controller `04B038FEC` is in the same `04B0xx` range as AHU-14's object `04B016FEC`, both on `JL-BLDG57-SNE04/FC-B`.
  - **Caveat**: MH102 does NOT actually draw any ductwork into the 2170/2180A/2190A/2200 area — that part of the sheet is blank. So we know the room is filed on this sheet/system, but we have never actually seen the pipe traced from AHU-14 to the 2170 box on paper.
- **AHU-1E / AHU-3 candidates (complication)**: `Z:\Duct Prints\B01 D\MH112 UNIT 4 MECHANICAL DUCTWORK ROOF PLAN.pdf` (filed under B01 D but actually Project 2882.63, 2011, Unit 5 Bioinformatics rooftop project) has an "Air Handler Airflow Balance Schedule" that allocates **existing Unit 4, Second Floor** airflow across THREE different air handlers:
  - AHU-14: (not in this schedule — separate 2003 project)
  - AHU-1E: 1,200 cfm to Unit 4 2nd floor
  - AHU-3: 2,370 cfm to Unit 4 2nd floor
  - AHU-2E: 0 cfm to Unit 4 2nd floor (its Unit 4 allocation is all 1st/3rd floor)
  - We checked the full 18-page `B01 E\Mechanical.pdf` set from this same 2011 project — it only documents Unit 5's own floors. **There is no floor-level plan anywhere in this set showing where AHU-1E's or AHU-3's Unit-4-2nd-floor air actually lands.**
- **Bottom line on AHU identity**: documentation is genuinely inconclusive. At least 3 different air handlers (AHU-14, AHU-1E, AHU-3) have documented ties to Unit 4's 2nd floor, and none of the paper trail confirms which one (if any beyond AHU-14) reaches the 2075–2187 cluster specifically. AHU-10 is the only one cleanly ruled out.
- **Not yet done**: check Metasys's own navigation-tree parent for `04B038FEC` (its immediate parent folder in the point tree should name the actual serving AHU directly) — this would likely settle it faster than any more drawing research. Still outstanding as of this writing.
- **2007 renovation** (`Unit4.3rdFloorReno_06.02`, Project 288247) does not touch the 2075–2200 corridor — it covers telecom/video-conference/graphics/mailing offices elsewhere on the floor. Consistent with the theory that this specific area runs older, un-renovated equipment/ductwork.

## Live Metasys data pulled today

- **VAV "Rm 1075-1115"** (`1050020FAC`) — 5-zone unit including Rm 1115 (near VAV-11's documented service area per MH101). Object numbering (`10-series FAC`) does not match AHU-14's `04B0xx` trunk; embedded `AHU-1/AHU-2/EF-2 Status` points are most likely a standard JCI mirrored-status template, not evidence of a separate physical AHU (per [[feedback_trust_drawings_over_live_labels]] — documented drawings take precedence over live screen-label interpretation).
- **VAV Rm 2090** (documented as VAV-12 on MH102): Zone temp 69.9°F vs. 72°F cooling / 70°F heating setpoint — box is not currently under load. Damper only 35% open, Supply Flow 139 cfm vs. 375 cfm setpoint. **Not a valid comparison yet** — this box hasn't been tested near full-open under an active cooling call, so we can't tell if it would plateau early like 2170 does. Worth re-checking next time it's got a real cooling demand.

## Open questions for Wayne / next steps

1. **AHU identity is still not conclusively settled.** Recommend checking the Metasys navigation-tree parent of `04B038FEC` directly — fastest remaining way to resolve AHU-14 vs. AHU-1E vs. AHU-3.
2. **AHU-14's own discharge static pressure & fan speed** have not yet been checked — would immediately tell us AHU-wide capacity limit vs. isolated branch.
3. **Physical trace of the branch is difficult** — duct goes into a wall/chase near the box, no probe holes available for a static pressure survey. Duct size checked at one point (10", correctly sized) — worth checking 2-3 more points along the run for a narrower section, kink, or closed volume damper (VD) if accessible.
4. **Sibling box comparison (VAV-12/Rm 2090) inconclusive** — needs to be re-read during an actual cooling call, not at 35% damper command.
5. **Independent flow verification**: a flow-hood reading at the 2170 diffuser(s) compared against the BAS-reported ~400 cfm has not yet been done — would rule in/out a box sensor fault vs. a genuine restriction.
