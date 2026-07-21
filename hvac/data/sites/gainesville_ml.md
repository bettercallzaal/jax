# Gainesville, FL — ML Building (Alachua)

Second site, distinct from the Bar Harbor campus this toolkit otherwise tracks. Different BAS platform and naming convention — do not assume Metasys point-map conventions apply here.

## Platform
- **Niagara (Tridium) framework, Honeywell-branded front end** — not JCI Metasys.
- Room-level control via SAV boxes (Supply Air Valve — modulating supply/exhaust valve pair per room, similar role to a VAV/PIV box on the Bar Harbor side).
- Point naming example: `SAV 3-17 Rm 216 Proc 4` — SAV unit 3-17 serving Corridor 208 / Procedure Rm 4, tracking pair `GEV_3_16`.
- Controlled points per SAV box: Supply Valve (Box Flow / Eff Flow Spt), Exhaust Valve (Max/Min Flow Spt, Box Flow), Room Humidity, Room Temp, Room Spt, Room Press Spt/Out, Supply/Exhaust Dmpr Pos, Reheat Cmd (can show "Reheat Override"), Discharge Temp.
- Alarm console shows Source, Message Text, Priority — humidity alarms read like `SAV 3-XX Rm ### ..._RoomHumidity`, pressure alarms `..._RmPressure_Out`.

## Contacts
- **W.W. Gay Mechanical (WWG)** — controls service contractor:
  - Mark Garcia — Controls Service Manager, MGarcia@wwgmc.com, 352-264-2607
  - Conner T. Townsend — field tech, ctownsend@wwgmc.com
  - Ken Hovey — field tech (remote access support), khovey@wwgmc.com
- **Concept Companies** — site coordination:
  - Sonia Hopewell — Site Coordinator, shopewell@conceptcompanies.net, 352-440-4932
  - David Stockman, Jonathan Jury — also on site coordination threads
- Jesse Hinkle (JAX) — on-site contact, flagged the humidity issue by hand-held reader before it showed on BAS.

## 2026-07-21 — Widespread Room Humidity + Procedure Rm 4 sensor issue

**Procedure Rm 4 (SAV 3-17, Rm 216):**
- Room Humidity reading 88-94% RH, Room Temp 64.0°F against a 69.0°F setpoint (both flagged red/critical on the Honeywell graphic).
- Reheat Cmd shows 100% via a **Reheat Override**, but Discharge Temp is only 57.3°F and room temp hasn't recovered — reheat commanded to max isn't producing expected heat output. Worth checking hot water flow/valve operation at this box, not just assuming the override is doing its job because it's commanded on.
- Alarm history: last real alarm logged 7/20 ~10:11 AM at 71% RH; by the time Jesse Hinkle's team caught it by hand-held reader on 7/21, it was up to 94% RH with no new BAS alarm in between — sensor/alarm reporting gap, not just a slow-moving trend. Needs a check on whether the sensor itself is faulted or if it's an alarm-routing/dead-band issue.

**Building-wide pattern:** in a single ~45 minute window (7/21, 9:20-10:05 AM), Room Humidity alarms fired across many different rooms/SAVs: Rm 316, 240A, 314, 240, 214, 311, 241 (x2, Cell Bio and Lab 2), 220, 215, 217, 312. Two Room Pressure alarms in the same window (Rm 316, Rm 314 Elev Vest). That many rooms alarming near-simultaneously points toward a central air-handling/plant issue (cooling coil overshoot, chilled water valve, or a building-wide dehumidification sequence problem) rather than each room's local equipment failing independently — worth ruling out the central plant before treating this as N separate room-level faults.

**Action:** Conner (WWG) scheduled on site morning of 7/22 to investigate. Zaal to connect with him on site to observe the Niagara-side diagnostic workflow.

**Punch list for Conner (7/22):**
1. Procedure Rm 4 — confirm whether the Room Humidity sensor is actually faulted, or if this is an alarm-routing/deadband gap (room kept getting worse 7/20-7/21 with only one alarm logged).
2. Procedure Rm 4 — Reheat Override is commanding 100% but Discharge Temp (57.3°F) and Room Temp (64°F) both suggest it isn't actually heating. Check hot water valve/flow at that reheat coil.
3. Check whether the cluster of Room Humidity alarms across ~12 rooms this morning traces back to a shared air handler/plant issue (cooling coil, chilled water valve, dehumidification sequence) rather than treating each room individually.
4. Provide equipment recommendations (dehumidifier type/capacity or other) for rooms with chronic/recurring humidity issues, per Sonia's request.
5. Exhaust damper stuck at 0% — Holding Room 3 (separate item, flagged in the 7/21 email to Mark/Sonia).
6. General: confirm which trends aren't reporting data to the server — flagged separately, worth checking while on site since it may be related to the same alarm-reporting gap seen on Procedure Rm 4.
