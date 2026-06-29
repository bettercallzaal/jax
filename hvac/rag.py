"""
HVAC Knowledge RAG — retrieval-augmented generation over the HVAC Field Toolkit.

Ingests all module knowledge into text chunks, embeds them (sentence-transformers
with TF-IDF fallback), retrieves top-k relevant chunks for a query, then calls
Claude with prompt caching so the knowledge base stays in the cache across calls.
"""

from __future__ import annotations

import json
import math
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Document chunks — structured HVAC knowledge extracted from toolkit modules
# ---------------------------------------------------------------------------

@dataclass
class Chunk:
    id: str
    source: str          # module name
    topic: str           # human-readable category
    text: str            # the retrievable content
    tags: list[str] = field(default_factory=list)


def _build_corpus() -> list[Chunk]:
    """Extract all HVAC knowledge into structured chunks."""
    chunks: list[Chunk] = []

    # --- diagnostics: reheat faults ---
    chunks.append(Chunk(
        id="diag-rht-001",
        source="diagnostics",
        topic="Reheat Fault: Hot discharge with zero reheat command",
        tags=["reheat", "hot_water", "valve", "fault"],
        text="""FAULT RHT-001: High discharge temp with zero reheat command — coil leaking heat.
Severity: HIGH.
Symptom: Discharge air temp >= 80°F but reheat output <= 5% (zero commanded).
This is the classic stuck-open or leaking valve signature.

Likely causes:
- Hot water valve stuck open or failed open (most common)
- Valve actuator failed or disconnected — valve defaulting open
- Valve bypass / manual override left open
- Balancing valve set too high — residual heat transfer even when 'closed'
- Wrong valve fail-safe: reheat valves should fail-CLOSED (power-close), not fail-open
- Control signal wiring shorted — always commanding open
- DDC controller output card failed — stuck at high voltage

Next steps:
1. Feel HW supply and return pipes at coil — both pipes hot = valve is leaking
2. Command valve to 0% from BAS/controller, measure pipe temps again
3. Physically inspect valve actuator for disconnection or damage
4. Check DDC output signal with multimeter (typical: 2–10 VDC or 4–20 mA)
5. If signal is correct but valve doesn't move → replace actuator
6. If signal is wrong → trace back to DDC output card
7. Close upstream manual isolation valve to confirm coil as heat source

Confirmation: Closing manual isolation valve — if discharge temp drops, valve/coil is the heat source."""
    ))

    chunks.append(Chunk(
        id="diag-rht-002",
        source="diagnostics",
        topic="Reheat Fault: Electric reheat stuck on",
        tags=["reheat", "electric", "contactor", "fault"],
        text="""FAULT RHT-002: High discharge temp with zero electric reheat command — contactor or SCR stuck closed.
Severity: HIGH.
Symptom: Discharge air warm despite electric reheat commanded off.

Likely causes:
- Contactor welded closed (failed energized)
- SCR (silicon controlled rectifier) failed in 'on' state
- High-limit thermostat or safety relay bypassed
- Wiring fault — always energizing heating element

Next steps:
1. De-energize panel — check if discharge temp drops
2. Measure voltage across heating element with AHU running
3. Inspect contactors for welding/pitting
4. Check SCR control board for burn marks
5. Verify high-limit thermostat is not bypassed"""
    ))

    chunks.append(Chunk(
        id="diag-rht-003",
        source="diagnostics",
        topic="Reheat Fault: Full command but no temperature rise",
        tags=["reheat", "valve", "no_heat", "fault"],
        text="""FAULT RHT-003: Reheat at full command (>=80%) but no temperature rise across coil (ΔT < 5°F).
Severity: HIGH.
Symptom: Valve commanded open but discharge temp does not rise above supply air temp.

Likely causes:
- Hot water valve stuck closed or actuator failed-closed
- No hot water supply to system (plant off, pump down, valve isolated)
- Hot water supply temp too low (boiler setpoint issue, mixing valve problem)
- Coil fouled/clogged — restricted flow
- Air trapped in coil (needs purging)
- Electric: heating element failed open, breaker tripped, fuse blown

Next steps:
1. Verify hot water plant is running and supply temp (should be 120–180°F)
2. Check valve actuator — command 100%, physically verify valve shaft rotates
3. Measure HW supply/return pipe temps — if both same = no flow through coil
4. Open air bleed on coil if present
5. Check upstream/downstream isolation valves are open
6. Electric: check breaker, fuse, and element continuity with multimeter"""
    ))

    chunks.append(Chunk(
        id="diag-hws-001",
        source="diagnostics",
        topic="Hot Water Supply Temperature Too Low",
        tags=["hot_water", "boiler", "temperature", "fault"],
        text="""FAULT HWS-001: Hot water supply temperature too low (< 100°F).
Severity: MEDIUM.

Likely causes:
- Boiler setpoint too low or boiler fault
- Outdoor air reset (OAR) driving supply temp down aggressively
- Mixing valve (3-way) set wrong
- Heat exchanger fouled
- High system demand — not enough boiler capacity

Next steps:
- Check boiler plant status and setpoint (typical heating supply: 120–180°F)
- Review OAR schedule — may be appropriate at current outdoor temp
- Verify mixing valve position and setpoint
- Check heat exchanger condition"""
    ))

    chunks.append(Chunk(
        id="diag-hws-002",
        source="diagnostics",
        topic="Hot Water Coil Delta-T Too High — Restricted Flow",
        tags=["hot_water", "coil", "flow", "strainer"],
        text="""FAULT HWS-002: Hot water coil ΔT > 30°F — restricted flow through coil.
Severity: MEDIUM.
High ΔT means water is giving up more heat than expected, usually from restricted flow (less GPM, same heat load).

Likely causes:
- Coil partially fouled or clogged
- Valve not fully opening — check actuator
- System pump issue — low flow / cavitation
- Strainer clogged on coil supply line

Next steps:
- Check coil strainer — clean if dirty (measure ΔP across strainer)
- Verify pump operation and flow rates
- Command valve to 100% and re-measure pipe temps
- Check system balancing valves"""
    ))

    chunks.append(Chunk(
        id="diag-hws-003",
        source="diagnostics",
        topic="Hot Water Coil Delta-T Near Zero with Reheat Commanded",
        tags=["hot_water", "coil", "no_flow", "pump", "fault"],
        text="""FAULT HWS-003: Hot water coil ΔT near zero (< 5°F) with reheat > 50% commanded.
Severity: HIGH.
Near-zero ΔT with valve commanded open means NO flow through the coil.

Likely causes:
- Valve stuck closed — actuator not opening
- Isolation valves closed (supply or return)
- System pump not running
- Coil completely blocked

Next steps:
- Verify pump status (check VFD, breaker, rotation)
- Check all isolation valves are open (manual ball valves, butterfly valves)
- Command valve open and verify actuator physically moves
- Check differential pressure across coil"""
    ))

    chunks.append(Chunk(
        id="diag-ctl-001",
        source="diagnostics",
        topic="Control Signal vs Valve Position Mismatch",
        tags=["controls", "actuator", "signal", "DDC"],
        text="""FAULT CTL-001: Control signal vs. valve output mismatch > 15%.
Severity: MEDIUM.
The DDC is commanding a position but the valve/actuator is not following.

Likely causes:
- Actuator not responding to signal (mechanical failure)
- Signal wiring issue (broken wire, bad connection)
- DDC point misconfigured (wrong range, wrong output type)
- Actuator needs calibration (may have drifted)

Next steps:
- Measure signal at actuator terminals with multimeter
- Verify DDC output range matches actuator input range (0–10VDC or 4–20mA)
- Check for loose terminals or corroded connections
- Perform actuator stroke test (full open, full close)"""
    ))

    chunks.append(Chunk(
        id="diag-zone-temp",
        source="diagnostics",
        topic="Zone Temperature Comfort Complaint",
        tags=["zone", "comfort", "temperature", "setpoint"],
        text="""FAULT ZN-001: Zone comfort complaint — room temperature more than 3°F from setpoint.
Severity: HIGH if > 6°F off, MEDIUM if 3–6°F off.

Likely causes (warm room):
- Heating system fault: reheat valve stuck open, radiation valve stuck open
- Sensor error or offset — room sensor reading too cold, commanding more heat
- High internal loads (equipment, occupants, solar gain)
- Envelope/insulation issue (exterior wall, window, roof)
- Adjacent zone cross-talk (heat bleeding from neighboring space)

Likely causes (cold room):
- Cooling not working: chilled water unavailable, compressor off
- Low airflow: VAV box stuck at minimum, duct disconnected
- Supply air temp too warm (AHU issue)

Next steps:
1. Verify room sensor with independent calibrated thermometer
2. Check zone valve/damper command vs. position in DDC
3. Review recent setpoint changes and scheduling
4. Inspect for obvious heat sources or infiltration"""
    ))

    chunks.append(Chunk(
        id="diag-zone-cfm",
        source="diagnostics",
        topic="Low Zone Airflow",
        tags=["zone", "airflow", "CFM", "VAV", "damper"],
        text="""FAULT ZN-002: Low airflow — supply CFM < 70% of design CFM.
Severity: MEDIUM.

Likely causes:
- VAV box stuck at minimum position or failed minimum stop
- Duct obstruction or disconnected duct section
- Low AHU static pressure (VFD speed too low, duct leakage)
- Dirty filters — high resistance across filter bank
- VAV actuator failed

Next steps:
- Measure static pressure at AHU discharge and at zone branch
- Inspect VAV box actuator and damper blade position
- Check filter pressure drop (clean: 0.1–0.2\" WC, dirty: > 0.5\" WC)
- Verify AHU fan speed / VFD setpoint
- Use flow hood or pitot traverse to measure actual CFM"""
    ))

    chunks.append(Chunk(
        id="diag-zone-co2",
        source="diagnostics",
        topic="High CO2 — Inadequate Ventilation",
        tags=["CO2", "ventilation", "IAQ", "OA_damper"],
        text="""FAULT ZN-003: High CO2 > 1100 ppm — inadequate ventilation per ASHRAE 62.1.
Severity: HIGH if > 1500 ppm, MEDIUM if 1100–1500 ppm.

ASHRAE 62.1 guideline: CO2 should not exceed ~1100 ppm in occupied spaces
(approximately 700 ppm above 420 ppm outdoor baseline).

Likely causes:
- Insufficient outside air quantity or OA fraction
- DCV (demand control ventilation) not functioning correctly
- CO2 sensor fault — needs calibration
- High occupancy beyond design (e.g., conference room overloaded)
- OA damper stuck closed or at minimum

Next steps:
- Check OA damper position and command in DDC
- Verify CO2 sensor calibration (outdoor air calibration = ~420 ppm)
- Review minimum OA setpoints and DCV logic in DDC
- Increase OA manually as immediate measure
- Audit occupancy vs. design ventilation rates"""
    ))

    chunks.append(Chunk(
        id="diag-zone-humidity",
        source="diagnostics",
        topic="Zone Humidity Out of Range",
        tags=["humidity", "RH", "mold", "dehumidification"],
        text="""FAULTS ZN-004 (high humidity) and ZN-005 (low humidity).

HIGH HUMIDITY (> 65% RH) — Severity: HIGH (mold risk above 65%):
Likely causes:
- Cooling coil leaving air too warm — not dehumidifying
- Overcooled space (thermostat satisfied before dehumidification complete)
- No mechanical dehumidification
- Infiltration from high-humidity source (roof leak, foundation, door seals)

Next steps:
- Check cooling coil supply air temp and dew point (target SAT ≤ 52°F for dehumidification)
- Verify chilled water supply temp (typically ≤ 44°F CHWS for dehumidification)
- Check for envelope infiltration or plumbing leaks

LOW HUMIDITY (< 20% RH) — Severity: LOW (comfort/static issues):
Likely causes:
- No humidification system or humidifier off/failed
- High OA fraction in winter without humidity control (dry outdoor air)

Next steps:
- Check humidifier status and setpoint
- Verify OA fraction and preheat coil operation"""
    ))

    # --- JCI Metasys ---
    chunks.append(Chunk(
        id="metasys-point-map",
        source="jci_metasys",
        topic="Metasys VAV+HW Reheat Point Naming",
        tags=["Metasys", "VAV", "point_names", "JCI"],
        text="""JCI METASYS POINT NAMING — VAV Box with Hot Water Reheat

Airflow points:
  Airflow (CFM):          ZN-T / AHU-VAV-{box}-CFM
  Damper position (%):    ZN-T / AHU-VAV-{box}-DMPR-POS
  Damper command (%):     ZN-T / AHU-VAV-{box}-DMPR-CMD
  Min CFM setpoint:       ZN-T / AHU-VAV-{box}-CFM-MIN
  Max CFM setpoint:       ZN-T / AHU-VAV-{box}-CFM-MAX
  Design CFM:             ZN-T / AHU-VAV-{box}-CFM-DES

Temperature points:
  Zone temperature (°F):  ZN-T / AHU-VAV-{box}-ZN-T
  Zone setpoint (°F):     ZN-T / AHU-VAV-{box}-ZN-SP
  Discharge air temp:     ZN-T / AHU-VAV-{box}-DAT
  Supply air temp (AHU):  AHU-{ahu}-SAT

Reheat valve points:
  HW valve command (%):   ZN-T / AHU-VAV-{box}-HW-VLV-CMD
  HW valve position (%):  ZN-T / AHU-VAV-{box}-HW-VLV-POS
  HW supply temp:         HW-SUPPLY-T
  HW return temp:         HW-RETURN-T

Mode points:
  Zone mode:              ZN-T / AHU-VAV-{box}-MODE
    (0=Unoccupied, 1=Occupied, 2=Standby, 3=Warmup, 4=Cooldown, 5=Purge)
  Control mode:           ZN-T / AHU-VAV-{box}-CTRL-MODE
    (1=Cooling, 2=Deadband, 3=Heating)

Navigation in Metasys Site Director:
  Focus → Equipment → VAV-{box} → View"""
    ))

    chunks.append(Chunk(
        id="metasys-sequence",
        source="jci_metasys",
        topic="VAV+HW Reheat Sequence of Operation",
        tags=["VAV", "reheat", "sequence", "Metasys", "occupied", "unoccupied"],
        text="""VAV BOX WITH HOT WATER REHEAT — Sequence of Operation (JCI Metasys)

OCCUPIED MODE:
  Cooling (Zone T > Cooling SP + deadband):
    - Damper modulates 0→100% to maintain zone temperature
    - HW reheat valve: 0% (closed)
    - Minimum CFM enforced (ventilation minimum, typically 20–30% of max)

  Dead Band (Cooling SP > Zone T > Heating SP):
    - Damper holds at minimum CFM position
    - HW reheat valve: 0% (closed)

  Heating (Zone T < Heating SP - deadband):
    - Damper drives to minimum CFM position (or heat minimum, may be higher)
    - HW reheat valve modulates 0→100% to maintain zone heating setpoint
    - If HW valve at 100% and zone still cold → call for additional heat

UNOCCUPIED MODE:
  - Damper at minimum or closed (per code)
  - HW reheat valve: On/Off (not modulating) at unoccupied setpoints
  - Typical unoccupied setpoints: 60°F heat / 85°F cool

FAULT CONDITIONS:
  - If DAT > high limit (typically 105°F): Override HW valve closed, alarm
  - If DAT < low limit (typically 45°F): Freeze protection, alarm AHU
  - If CFM sensor reading 0 with damper open: Airflow sensor fault"""
    ))

    chunks.append(Chunk(
        id="metasys-stuck-open",
        source="jci_metasys",
        topic="Metasys Diagnostic: Stuck-Open Reheat Valve Procedure",
        tags=["Metasys", "reheat", "valve", "diagnostic", "steps"],
        text="""METASYS DIAGNOSTIC PROCEDURE — VAV Box HW Reheat Stuck-Open Valve

Step 1: Navigate to VAV box object in Metasys Site Director
  Look for: HW-VLV-CMD vs HW-VLV-POS — command should be 0%; check if position matches
  Path: Focus → Equipment → VAV-{box} → View

Step 2: Check CTRL-MODE point
  Look for: Should show 'Deadband' or 'Cooling' if zone is warm.
  If showing 'Heating' — logic is commanding heat.
  Note: If CTRL-MODE=Heating with warm room → check zone sensor reading and setpoints

Step 3: Override HW valve to 0% in Metasys (operator override)
  Look for: Watch DAT point — if discharge temp drops within 2–3 minutes, valve was passing flow
  Path: Focus → VAV-{box} → HW-VLV-CMD → Override to 0

Step 4: Check override vs. feedback
  Look for: HW-VLV-CMD = 0%, HW-VLV-POS still showing >0? → actuator not responding to signal
  Note: Also possible that no position feedback is wired — POS always reads same as CMD

Step 5: Go physical — feel HW supply and return pipes at the VAV box coil
  Look for: Both pipes hot with CMD=0% → valve body stuck open or actuator disconnected
  Note: Pipe temp delta: Supply − Return should drop to <5°F if valve is truly closed

Step 6: Check actuator signal at terminal strip
  Look for: Metasys analog output: 0–10VDC (0%=2V, 100%=10V) or 4–20mA (0%=4mA)
  Measure with multimeter. If signal correct but valve doesn't move → replace actuator

Step 7: Clear override in Metasys, verify normal operation resumes
  Look for: Valve should modulate per heating demand, DAT within normal range (55–85°F)
  Note: Document findings and override removal time in Metasys activity log"""
    ))

    chunks.append(Chunk(
        id="metasys-fault-dat-high",
        source="jci_metasys",
        topic="Metasys Fault: High Discharge Temp with Zero Valve Command",
        tags=["Metasys", "DAT", "valve", "fault", "DDC_output"],
        text="""METASYS FAULT PATTERN: DAT_HIGH_HW_ZERO
Symptom: Discharge air temp high (> 85°F), HW valve command at 0%.

Likely causes:
1. Valve stuck open / actuator failed — valve leaking hot water regardless of command
2. Valve wired backwards (0V=open, 10V=closed) — check actuator documentation
3. DDC output failed HIGH — check controller output module

Metasys path: Equipment → VAV-{box} → Points: DAT, HW-VLV-CMD, HW-VLV-POS, CTRL-MODE"""
    ))

    chunks.append(Chunk(
        id="metasys-fault-zone-warm-cool",
        source="jci_metasys",
        topic="Metasys Fault: Zone Warm with Valve Closed and Cooling Mode Active",
        tags=["Metasys", "cooling", "damper", "CFM", "AHU", "fault"],
        text="""METASYS FAULT PATTERN: ZONE_WARM_VALVE_ZERO_MODE_COOL
Symptom: Zone warm, HW valve 0%, control mode = Cooling.
This means the system is NOT commanding heat but zone is warm — cooling is insufficient.

Likely causes:
1. Cooling not working or insufficient cooling supply air from AHU
2. Damper not opening — check CFM vs. damper command (DMPR-CMD vs. CFM)
3. Supply air temp too high from AHU (AHU cooling not working, chilled water unavailable)

Metasys path: Equipment → VAV-{box} → DMPR-CMD, CFM, AHU-SAT"""
    ))

    chunks.append(Chunk(
        id="metasys-fault-dat-sensor",
        source="jci_metasys",
        topic="Metasys Fault: Discharge Air Temp Sensor Fault",
        tags=["Metasys", "DAT", "sensor", "fault", "reliability"],
        text="""METASYS FAULT PATTERN: DAT_SENSOR_FAULT
Symptom: DAT reading stuck at a fixed value or out of range.

Likely causes:
1. Sensor disconnected or shorted (Metasys will show default/last value or failsafe)
2. Sensor location wrong — in dead air pocket or near a heat source

Metasys path: Points → DAT → Properties → check Reliability field and last-update timestamp
If Reliability is not 'Reliable', the sensor has lost communication or is faulted."""
    ))

    chunks.append(Chunk(
        id="metasys-fault-cfm-zero",
        source="jci_metasys",
        topic="Metasys Fault: Zero Airflow with Damper Open",
        tags=["Metasys", "CFM", "airflow", "pitot", "damper", "AHU", "fault"],
        text="""METASYS FAULT PATTERN: CFM_ZERO_DAMPER_OPEN
Symptom: Airflow reads 0 CFM with damper commanded open.

Likely causes:
1. Pitot tube clogged (common in dusty or construction environments)
2. Differential pressure transducer failed (no output)
3. AHU fan off — no supply air in the duct
4. Damper actuator failed — blade not moving despite command

Metasys path: Equipment → VAV-{box} → CFM, DMPR-CMD, DMPR-POS"""
    ))

    # --- ASHRAE Standards ---
    chunks.append(Chunk(
        id="ashrae-621-vent",
        source="standards",
        topic="ASHRAE 62.1 Minimum Outdoor Air — Ventilation Rate Procedure",
        tags=["ASHRAE", "62.1", "ventilation", "outdoor_air", "CFM"],
        text="""ASHRAE 62.1 VENTILATION RATE PROCEDURE — Minimum Outdoor Air Requirements

Formula: Voz = (Rp × N + Ra × A) / Ev
  Rp = people component (CFM/person)
  N  = number of occupants
  Ra = area component (CFM/ft²)
  A  = floor area (ft²)
  Ev = ventilation effectiveness (1.0 for most systems)

Selected occupancy rates (ASHRAE 62.1-2019 Table 6.2.2.1):
  Office:           5 CFM/person + 0.06 CFM/ft²
  Conference room:  5 CFM/person + 0.06 CFM/ft²  (50 people/1000 ft² default density)
  Classroom:       10 CFM/person + 0.12 CFM/ft²  (35 people/1000 ft²)
  Lab (general):   10 CFM/person + 0.18 CFM/ft²
  Hospital patient: 25 CFM/person + 0.06 CFM/ft²
  Lobby:           7.5 CFM/person + 0.06 CFM/ft²
  Gym:             20 CFM/person + 0.18 CFM/ft²
  Retail:          7.5 CFM/person + 0.12 CFM/ft²
  Restroom:        0 CFM/person + 0.18 CFM/ft²
  Parking garage:  0 CFM/person + 0.75 CFM/ft²

CO2 guidelines:
  Outdoor baseline: ~420 ppm (2024)
  ASHRAE 62.1 comfort limit: ~1100 ppm (700 ppm above outdoor)
  OSHA 8-hr PEL: 5000 ppm"""
    ))

    chunks.append(Chunk(
        id="ashrae-55-comfort",
        source="standards",
        topic="ASHRAE 55 Thermal Comfort Zones",
        tags=["ASHRAE", "55", "comfort", "temperature", "humidity", "air_velocity"],
        text="""ASHRAE 55 THERMAL COMFORT — Acceptable Conditions

Summer comfort zone:
  Temperature: 74–80°F dry bulb
  Relative Humidity: 30–60% RH
  Air velocity: < 30 fpm (0.15 m/s) in occupied zone

Winter comfort zone:
  Temperature: 68–74°F dry bulb
  Relative Humidity: 30–60% RH
  Air velocity: < 30 fpm (0.15 m/s) in occupied zone

Notes:
- Elevated air velocity (up to ~60 fpm) can allow warmer temp setpoints (ASHRAE 55-2020 elevated air speed)
- Radiant asymmetry limits: < 10°F ceiling-to-floor, < 5°F wall-to-wall
- Floor surface temp: 65–84°F for occupants in contact
- Draft complaints most common at neck level (seated: 4.3 ft, standing: 6.6 ft)

Common issues:
- Rooms near perimeter windows often need supplemental heating in winter (radiant cold glass)
- Rooms in cooling mode with high supply air velocity may cause draft complaints even within temp limits"""
    ))

    chunks.append(Chunk(
        id="ashrae-901-sat-reset",
        source="standards",
        topic="ASHRAE 90.1 Supply Air Temperature Reset",
        tags=["ASHRAE", "90.1", "energy", "SAT_reset", "supply_air"],
        text="""ASHRAE 90.1 SUPPLY AIR TEMPERATURE RESET

Purpose: Raise supply air temperature when zone cooling loads are reduced, saving both
cooling energy (less chiller work) and simultaneous reheat energy.

Logic: Reset SAT upward by 1°F per 5°F that the zone temperature drops below setpoint.
  Base SAT: typically 55°F
  Maximum SAT: typically 62°F
  Reset = max(0, (zone_setpoint - zone_temp) / 5)
  Target SAT = min(max_SAT, base_SAT + reset)

Example: Zone setpoint 72°F, zone temp 68°F (cold) → reset = (72-68)/5 = 0.8°F → SAT = 55.8°F

Economizer (enthalpy-based, ASHRAE 90.1):
  Enable when: outdoor enthalpy < return air enthalpy AND outdoor temp < lockout temp (typically 75°F)
  Disable (lockout) when: outdoor temp or enthalpy exceeds threshold

Chilled water supply temp reset (ASHRAE 90.1):
  Raise CWST 1°F per 2°F rise in return water temperature above 54°F baseline
  Base CWST: 44°F, Maximum CWST: 54°F"""
    ))

    # --- Commissioning ---
    chunks.append(Chunk(
        id="cx-pre-startup",
        source="commissioning",
        topic="Pre-Startup Commissioning Checklist",
        tags=["commissioning", "startup", "checklist", "mechanical", "electrical", "hydronic", "controls"],
        text="""PRE-STARTUP COMMISSIONING CHECKLIST (ASHRAE Guideline 1.1)

MECHANICAL (critical items marked *):
  M01* All ductwork connections tight and sealed (no visible gaps)
  M02  Equipment mounting bolts torqued to spec
  M03  Vibration isolators installed and equally compressed
  M04* Refrigerant lines: no kinks, insulation intact, proper slope
  M05* Control valves installed in correct flow direction (arrow visible on body)
  M06* Filters installed with correct airflow direction
  M07  All access panels closed and secured
  M08  Outdoor unit clear of obstructions (≥ 3 ft clearance)
  M09  Drain pan clean and drain line clear
  M10  Coil fins straight (straighten if bent)

ELECTRICAL (critical items marked *):
  E01* Breaker amperage matches equipment nameplate (within ±10%)
  E02* Voltage at equipment matches nameplate
  E03* Ground and neutral properly bonded
  E04  3-phase rotation correct (verified with phase rotation meter)
  E05  Control wiring complete, shielded for sensor cables
  E06  24V transformer installed and fused
  E07  Thermostat/sensor wiring identified and labeled
  E08  Motor capacitors correct rating (run/start)

HYDRONIC (critical items marked *):
  H01* System filled to proper pressure (typically 15–30 psi / 1–2 bar)
  H02* Air purged from system (manual bleeder valves opened at high points)
  H03* Pump rotation correct (no cavitation noise)
  H04  Expansion tank pre-charge set for system pressure
  H05* All isolation valves open (supply and return)
  H06  Strainers clean (record delta-P across strainer)
  H07  Balancing valves at design position
  H08  Flow meter functional (if installed)

CONTROLS & SENSORS (critical items marked *):
  C01* All sensors in place (temperature, humidity, pressure, CO2)
  C02* Sensor calibration verified (ice bath / reference thermometer)
  C03* DDC controller powered, network connection verified
  C04  System time synchronized (for scheduling)
  C05  Battery backup operational
  C06* All DDC outputs functional (test each analog and binary output)
  C07  Setpoints documented and entered in BAS
  C08  Occupied/unoccupied schedule verified
  C09* High-limit safeties functional (simulate and verify shutdown)
  C10  Economizer damper operation verified"""
    ))

    chunks.append(Chunk(
        id="cx-startup-sequence",
        source="commissioning",
        topic="HVAC Startup Sequence Steps",
        tags=["commissioning", "startup", "sequence", "cooling", "heating", "balancing"],
        text="""HVAC STARTUP SEQUENCE (5 steps)

Step 1 — Blower Only (~15 min):
  Actions: Start supply fan only (disable heating/cooling), listen for rubbing/grinding,
    verify airflow at all supply/return grilles, check for ductwork vibration
  Pass criteria: No unusual mechanical noise, air movement confirmed at all outlets, filter ΔP < 0.3" WC

Step 2 — Cooling Stage Startup (~20 min):
  Actions: Enable mechanical cooling, monitor discharge pressure, verify coil outlet temp drops,
    check suction pressure stability, measure supply air ΔT, verify condensate drain flowing
  Pass criteria: Supply air temp drops to setpoint (~55°F), suction pressure stable,
    superheat 8–15°F, no high-pressure fault

Step 3 — Heating Stage Startup (~20 min):
  Actions: Enable heating/disable cooling, verify HW pump running and temps rise,
    monitor current draw (electric), check flame sensor (gas), measure discharge temp rise
  Pass criteria: Discharge temp rises to heating setpoint, HW ΔT 10–20°F at design flow,
    no high-limit trips, modulation smooth (no hunting)

Step 4 — Controls Verification (~30 min):
  Actions: Raise setpoint 2°F → heating should activate within 2 min; lower setpoint 2°F → cooling within 2 min;
    verify deadband (no simultaneous heating AND cooling); test DCV (blow CO2 near sensor);
    force high-limit fault — system should shut down and alarm
  Pass criteria: Heating/cooling responds within 2 min, lockout proven, alarms annunciate in BAS

Step 5 — Airflow Balancing (~60 min):
  Actions: Measure CFM at each supply diffuser (flow hood or pitot traverse),
    measure static pressure at AHU supply/return plenums, adjust VAV/branch dampers to design,
    verify return airflow balanced with supply
  Pass criteria: Each diffuser within ±10% of design CFM, supply/return within 10% of each other"""
    ))

    chunks.append(Chunk(
        id="cx-sensor-calibration",
        source="commissioning",
        topic="Field Sensor Calibration Procedures",
        tags=["commissioning", "calibration", "sensor", "temperature", "pressure", "humidity", "CO2"],
        text="""FIELD SENSOR CALIBRATION PROCEDURES

TEMPERATURE SENSOR:
  Ice bath method (32°F reference):
    1. Fill container with crushed ice + distilled water (slurry)
    2. Wait 5–10 min for thermal equilibrium
    3. Insert calibrated reference thermometer (±0.5°F) and sensor probe
    4. Hold both vertical, 2–3 inches deep in slurry
    5. Compare readings — adjust if error > ±2°F
    6. Document: technician, date, sensor ID, reading before/after

  Boiling water method (212°F reference at sea level):
    - Adjust 212°F by -0.5°F per 1000 ft elevation

PRESSURE SENSOR:
  1. Zero sensor at atmospheric pressure (disconnect from system)
  2. Apply test pressures: 25%, 50%, 75%, 100% of sensor range
  3. Use deadweight tester (±0.5%) as reference
  4. Adjust zero and span if error > ±2% at any point
  5. Recommended recalibration: every 6–12 months

HUMIDITY SENSOR:
  1. Compare to calibrated psychrometer in same air mass
  2. Acceptable field tolerance: ±5% RH
  3. If error > ±5%: Send to factory calibration service
  4. Salt solution reference: LiCl = 11.3% RH, NaCl = 75.3% RH

CO2 SENSOR:
  1. Take sensor to outdoor location away from traffic/HVAC exhausts
  2. Wait 5 minutes — outdoor CO2 ≈ 420 ppm (2024 baseline)
  3. Press calibration button or set offset in BAS to read 420 ppm
  4. Verify alarm setpoints: Warning ~1000 ppm, High ~1500 ppm
  5. Recommended recalibration: Annually"""
    ))

    # --- Refrigeration ---
    chunks.append(Chunk(
        id="refrig-superheat",
        source="refrigeration",
        topic="Refrigerant Superheat and Subcooling Diagnostics",
        tags=["refrigeration", "superheat", "subcooling", "R410A", "TXV", "charge"],
        text="""REFRIGERANT SUPERHEAT AND SUBCOOLING DIAGNOSTICS

Superheat = Suction line temperature − Saturation temperature at suction pressure
  Normal range: 8–15°F (target ~12°F)
  LOW SUPERHEAT (< 5°F): FAULT — Risk of liquid slugging compressor.
    Causes: Overcharge, TXV set too open, liquid flooding back
  HIGH SUPERHEAT (> 25°F): FAULT — System undercharged or TXV too restrictive.
    Causes: Low refrigerant charge, TXV hunting or stuck closed, restricted filter-drier

Subcooling = Saturation temperature at condensing pressure − Liquid line temperature
  Normal range: 5–15°F (target ~7°F)
  LOW SUBCOOLING (< 3°F): FAULT — Risk of flash gas at expansion device.
    Causes: Low charge, liquid line restriction (filter-drier plugged), oversized expansion valve
  HIGH SUBCOOLING (> 15°F): WARNING — System may be overcharged or condenser performance issues.

Compression ratio = Discharge pressure / Suction pressure
  Normal: 3–8:1
  HIGH (> 10:1): FAULT — Low suction or high discharge pressure
  HIGH (8–10:1): WARNING — Investigate condenser or charge

Discharge temperature limits:
  R-410A: Max 240°F  |  R-22: Max 240°F  |  R-32: Max 250°F  |  R-134a: Max 230°F"""
    ))

    chunks.append(Chunk(
        id="refrig-r410a-pt",
        source="refrigeration",
        topic="R-410A Pressure-Temperature Reference",
        tags=["refrigeration", "R410A", "P-T", "pressure", "temperature"],
        text="""R-410A SATURATION PRESSURE-TEMPERATURE TABLE (psia)

Temp (°F) → Pressure (psia)
  -20°F → 27.8    0°F → 48.3    20°F → 78.5    40°F → 121.7
   45°F → 135.0  50°F → 149.4   55°F → 165.2   60°F → 182.5
   70°F → 221.3  80°F → 265.8   90°F → 316.8   95°F → 344.8
  100°F → 374.2  105°F → 405.3  110°F → 438.2  120°F → 509.7
  130°F → 589.0  140°F → 676.0

High-pressure switch trip point: 400 psia (typical)
Low-pressure switch trip point: 30 psia (typical)

Typical field readings for 95°F outdoor / 75°F indoor:
  Suction pressure: ~140–160 psia (sat temp ~47–52°F)
  Discharge pressure: ~340–370 psia (sat temp ~93–98°F)
  Superheat target: 10–15°F at suction service valve
  Subcooling target: 6–10°F at liquid service valve"""
    ))

    chunks.append(Chunk(
        id="refrig-r22-pt",
        source="refrigeration",
        topic="R-22 Pressure-Temperature Reference",
        tags=["refrigeration", "R22", "P-T", "pressure", "temperature"],
        text="""R-22 SATURATION PRESSURE-TEMPERATURE TABLE (psia)

Temp (°F) → Pressure (psia)
  -20°F → 10.8   0°F → 21.1   20°F → 37.7   40°F → 63.6
   50°F → 80.9  60°F → 101.6  70°F → 126.0  80°F → 154.4
   90°F → 187.3  95°F → 205.5 100°F → 224.9 105°F → 245.6
  110°F → 267.6 120°F → 315.8 130°F → 370.0

High-pressure switch trip: 300 psia
Low-pressure switch trip: 20 psia
Note: R-22 production phased out; replacement options include R-407C, R-422D."""
    ))

    # --- Psychrometrics ---
    chunks.append(Chunk(
        id="psych-formulas",
        source="psychrometrics",
        topic="Key Psychrometric Formulas and Rules of Thumb",
        tags=["psychrometrics", "enthalpy", "humidity_ratio", "heat_transfer"],
        text="""KEY PSYCHROMETRIC FORMULAS (HVAC field use)

Sensible heat: Q_sensible = 1.1 × CFM × ΔT (BTU/hr)
  (at sea level; 1.1 = 60 min/hr × 0.075 lb/ft³ × 0.24 BTU/lb·°F)

Latent heat: Q_latent = 4840 × CFM × ΔW (BTU/hr)
  (ΔW = humidity ratio change, lb water/lb dry air)

Total heat: Q_total = 4.5 × CFM × Δh (BTU/hr)
  (Δh = enthalpy change, BTU/lb dry air)

Hot/chilled water coil: Q = 500 × GPM × ΔT (BTU/hr)
  (500 = 60 min/hr × 8.33 lb/gal × 1.0 BTU/lb·°F)

Enthalpy of moist air: h = 0.240 × T + W × (1061 + 0.444 × T) BTU/lb
  (T in °F, W in lb/lb)

Humidity ratio: W = 0.62198 × Pw / (Patm − Pw)
  (Pw = vapor pressure, Patm = atmospheric pressure, both same units)

Dew point: Use Magnus formula or psychrometric chart
  Rule of thumb: Dew point ≈ T - ((100 - RH) / 5) for T in °C

Sensible heat ratio (SHR) = Q_sensible / Q_total
  Typical office: SHR = 0.75–0.85
  High-latent spaces (gyms, restaurants): SHR = 0.50–0.70"""
    ))

    # --- JCI VA-7450 Series Actuator ---
    chunks.append(Chunk(
        id="actuator-va7450-install",
        source="equipment_datasheet",
        topic="JCI VA-7450 Series Electric Valve Actuator — Installation & Wiring",
        tags=["actuator", "VA-7450", "valve", "JCI", "wiring", "mounting", "proportional", "floating"],
        text="""JCI VA-7450 SERIES ELECTRIC VALVE ACTUATOR — Installation Instructions
Part No. 34-636-771 | Johnson Controls | For use with VG4000/VG5000 Series Zone Valves

MODELS:
  VA-7450-10011: On/Off or Floating Control — 24 VAC input signal
  VA-7452-90011: Proportional Control — 0 to 10 VDC input signal

WIRING (VA-7452-90011 Proportional):
  RED   → 24 VAC Power (hot)
  BLUE  → 24 VAC Common
  WHITE → 0–10 VDC Input Signal (+) from DDC controller

WIRING (VA-7450-10011 On/Off or Floating):
  BLUE  → Common
  WHITE → Up signal (24 VAC)
  RED   → Down signal (24 VAC)

VOLTAGE TEST POINTS (VA-7452-90011, 0–10 VDC, measure WHITE to BLUE):
  0%   command → 0.0 VDC
  50%  command → 5.0 VDC
  100% command → 10.0 VDC

MOUNTING PROCEDURE:
  1. Pipe the VG4000/VG5000 zone valve into the system first
  2. Confirm actuator is in fully up position (factory ships this way; if pre-powered, return to fully up)
  3. Place threaded coupler over valve stem and bonnet
  4. Rotate actuator body to desired position
  5. Hand tighten threaded coupler — DO NOT use a wrench (damages actuator)
  6. Minimum 7/8 in. (22 mm) clearance above actuator required
  7. Mount within 90° of vertical above valve body — beyond 90° allows moisture into actuator

JUMPER SETTINGS (VA-7452-90011 only — access via 1/8 in. flathead screwdriver):
  JP1: Anti-Sticking Cycle  — IN=On | OUT=Off (factory: Off)
  JP2+3: Input Signal Range — 0-10V / 5-10V / 0-5V (factory: 0–10 VDC)
  JP4: Valve Body Type      — IN=Three-Way | OUT=Two-Way (factory: Two-Way)
  JP5: Action               — IN=Direct (DA) | OUT=Reverse (RA) (factory: DA)
       DA: signal increase drives stem DOWN (closes N.O. valve)
       RA: signal increase drives stem UP (opens N.O. valve)
  JP6: Valve Normal Position — IN=PDTO (N.C.) | OUT=PDTC (N.O.) (factory: PDTC)
       PDTC = Push Down to Close = Normally Open valve (spring opens on power loss)
       PDTO = Push Down to Open  = Normally Closed valve (spring closes on power loss)

CRITICAL FOR REHEAT VALVES — JP6 FAIL-SAFE:
  Factory default JP6 = PDTC (Normally Open) → valve FAILS OPEN on power loss → room overheats.
  For hot water reheat, change JP6 to PDTO (Normally Closed) → valve FAILS CLOSED → safe.
  Leaking-by with valve commanded closed: check JP6 first — if PDTC with N.C. valve body,
  the spring is fighting the actuator and valve will never fully seal.

LED STATUS INDICATORS:
  Solid on      → Power present, motor not running
  Single flash  → Motor running (valve moving)
  Double flash  → End-of-stroke confirmation or anti-sticking cycle
  Off           → No power

AUTO-COMMISSIONING (VA-7452-90011):
  On first power application, actuator self-calibrates: drives stem DOWN for ~80 seconds,
  then moves to commanded signal position. Normal behavior — do not interrupt.

ANTI-STICKING CYCLE (JP1, optional):
  When enabled: performs one complete stroke every 24 hours to clear debris from valve seat.
  Actuator does not respond to DDC commands during this cycle.

TECHNICAL SPECS:
  Power:         24 VAC ±15%, 50/60 Hz, 2.7 VA, Class 2
  Output force:  21.5 lb (96 N) minimum
  Full stroke:   0.20 in. (5 mm), 65 seconds cycle time
  Rated cycles:  100,000
  Fluid temp:    35–203°F (2–95°C)
  Ambient:       32–122°F (0–50°C), noncondensing
  Cable:         22 AWG, 9.8 ft (3 m)
  Certifications: UL 873, CSA C22.2 No. 139, CE Mark"""
    ))

    chunks.append(Chunk(
        id="actuator-va7450-troubleshoot",
        source="equipment_datasheet",
        topic="JCI VA-7450 Actuator — Troubleshooting Leaking-By and Jumper Issues",
        tags=["actuator", "VA-7450", "valve", "leaking", "fail-safe", "PDTC", "PDTO", "jumper"],
        text="""JCI VA-7450 ACTUATOR — FIELD TROUBLESHOOTING

VALVE LEAKING BY WITH ACTUATOR COMMANDED CLOSED:
Three causes to check in order:

1. JP6 JUMPER WRONG FOR VALVE BODY (most overlooked):
   - Factory default JP6 = PDTC (N.O. = spring opens valve)
   - If your valve BODY is N.C. (PDTO type) but jumper is PDTC: spring and actuator fight each other
   - Actuator pushes down to OPEN an N.C. valve, but spring tries to CLOSE it → valve never fully seats
   - FIX: Change JP6 to match the actual valve body type. For reheat: PDTO (N.C., fail closed)

2. SIGNAL RANGE MISMATCH (JP2/JP3):
   - If DDC outputs 2–10V range but actuator jumpered for 0–10V:
     At DDC 0% command (2V), actuator sees ~20% position → never goes fully closed
   - FIX: Match JP2/JP3 to DDC output range, OR reconfigure DDC output to 0–10V

3. PHYSICAL VALVE SEAT ISSUE:
   - Debris on valve plug or seat (new valve or post-flush condition)
   - Anti-sticking cycle (JP1=ON) can help clear impurities
   - If seat is scored or damaged: replace valve body, not just actuator

VALVE NOT MOVING WITH CORRECT SIGNAL:
  - Confirm 24 VAC between RED and BLUE wires
  - Confirm signal voltage between WHITE and BLUE (0–10V at 0–100%)
  - LED should single-flash while motor runs; if solid-on with correct signal → actuator failed
  - Actuator does not respond during auto-commissioning, end-of-stroke, or anti-sticking cycle
    (double-flash LED indicates these cycles)

REPOSITIONING AFTER INSTALLATION:
  - Loosen threaded coupler, rotate actuator, hand-tighten — do NOT power actuator while loose"""
    ))

    return chunks


# ---------------------------------------------------------------------------
# Embedding backends
# ---------------------------------------------------------------------------

class TFIDFEmbedder:
    """Pure-Python TF-IDF embedder (stdlib + scikit-learn if available)."""

    def __init__(self):
        self._idf: dict[str, float] = {}
        self._vocab: list[str] = []
        self._fitted = False

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(r"[a-z0-9]+", text.lower())

    def fit(self, texts: list[str]) -> None:
        import math
        n = len(texts)
        df: dict[str, int] = {}
        for text in texts:
            words = set(self._tokenize(text))
            for w in words:
                df[w] = df.get(w, 0) + 1
        self._idf = {w: math.log((n + 1) / (c + 1)) + 1 for w, c in df.items()}
        self._vocab = sorted(self._idf.keys())
        self._fitted = True

    def _tf(self, tokens: list[str]) -> dict[str, float]:
        counts: dict[str, float] = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
        total = max(len(tokens), 1)
        return {w: c / total for w, c in counts.items()}

    def embed(self, text: str) -> list[float]:
        if not self._fitted:
            raise RuntimeError("Call fit() first")
        tokens = self._tokenize(text)
        tf = self._tf(tokens)
        vec = [tf.get(w, 0.0) * self._idf.get(w, 0.0) for w in self._vocab]
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed(t) for t in texts]


class SentenceTransformerEmbedder:
    """Wrapper around sentence-transformers for dense embeddings."""

    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(self.MODEL_NAME)

    def embed(self, text: str) -> list[float]:
        return self._model.encode(text, normalize_embeddings=True).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False).tolist()


def _make_embedder():
    """Return sentence-transformers if available, else TF-IDF."""
    try:
        emb = SentenceTransformerEmbedder()
        return emb, "sentence-transformers"
    except Exception:
        return None, "tfidf"


# ---------------------------------------------------------------------------
# Vector store
# ---------------------------------------------------------------------------

STORE_PATH = Path(__file__).parent / "data" / "rag_store.json"


@dataclass
class VectorStore:
    chunks: list[Chunk]
    embeddings: list[list[float]]
    embedder_type: str

    def save(self) -> None:
        STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "embedder_type": self.embedder_type,
            "chunks": [
                {"id": c.id, "source": c.source, "topic": c.topic, "text": c.text, "tags": c.tags}
                for c in self.chunks
            ],
            "embeddings": self.embeddings,
        }
        STORE_PATH.write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls) -> Optional["VectorStore"]:
        if not STORE_PATH.exists():
            return None
        data = json.loads(STORE_PATH.read_text())
        chunks = [Chunk(**c) for c in data["chunks"]]
        return cls(chunks=chunks, embeddings=data["embeddings"], embedder_type=data["embedder_type"])


def _cosine_sim(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def build_store(force: bool = False) -> VectorStore:
    """Build (or load from cache) the vector store."""
    if not force:
        store = VectorStore.load()
        if store:
            return store

    chunks = _build_corpus()
    emb, etype = _make_embedder()

    if emb is None:
        # TF-IDF path
        tfidf = TFIDFEmbedder()
        texts = [c.text for c in chunks]
        tfidf.fit(texts)
        embeddings = tfidf.embed_batch(texts)
        etype = "tfidf"
    else:
        embeddings = emb.embed_batch([c.text for c in chunks])

    store = VectorStore(chunks=chunks, embeddings=embeddings, embedder_type=etype)
    store.save()
    return store


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

@dataclass
class RetrievedChunk:
    chunk: Chunk
    score: float


def retrieve(query: str, store: VectorStore, top_k: int = 5,
             tag_filter: Optional[list[str]] = None) -> list[RetrievedChunk]:
    """Retrieve top-k chunks relevant to query."""
    emb, etype = _make_embedder()

    # Embed query with same embedder type as store
    if store.embedder_type == "tfidf" or emb is None:
        tfidf = TFIDFEmbedder()
        tfidf.fit([c.text for c in store.chunks])
        q_vec = tfidf.embed(query)
    else:
        q_vec = emb.embed(query)

    scored: list[RetrievedChunk] = []
    for chunk, emb_vec in zip(store.chunks, store.embeddings):
        if tag_filter and not any(t in chunk.tags for t in tag_filter):
            continue
        score = _cosine_sim(q_vec, emb_vec)
        scored.append(RetrievedChunk(chunk=chunk, score=score))

    scored.sort(key=lambda r: r.score, reverse=True)
    return scored[:top_k]


# ---------------------------------------------------------------------------
# Claude generation with prompt caching
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are JAX — an expert HVAC field technician assistant deployed at jax.org.
You help field technicians diagnose HVAC faults, interpret building automation system (BAS) readings,
apply ASHRAE standards, and troubleshoot refrigeration systems.

Answer concisely and practically. When you give diagnostic steps, number them.
Reference specific point names, temperatures, pressures, or code sections when relevant.
If the context provided is sufficient to answer, use it. If you need to make assumptions, state them."""


def ask(
    question: str,
    top_k: int = 5,
    store: Optional[VectorStore] = None,
    api_key: Optional[str] = None,
) -> str:
    """
    RAG query: retrieve relevant chunks, then generate with Claude + prompt caching.

    Uses cache_control on both the system prompt and the retrieved context block
    so repeated queries over the same knowledge base are served from cache.
    """
    import anthropic

    if store is None:
        store = build_store()

    results = retrieve(question, store, top_k=top_k)

    # Build the knowledge context block
    context_parts = []
    for r in results:
        context_parts.append(
            f"[Source: {r.chunk.source} | Topic: {r.chunk.topic}]\n{r.chunk.text}"
        )
    context_block = "\n\n---\n\n".join(context_parts)

    knowledge_message = (
        "RELEVANT HVAC KNOWLEDGE (retrieved for this query):\n\n"
        + context_block
    )

    client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": knowledge_message,
                        "cache_control": {"type": "ephemeral"},
                    },
                    {
                        "type": "text",
                        "text": f"\nQuestion: {question}",
                    },
                ],
            }
        ],
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
    )

    return response.content[0].text


def ask_stream(
    question: str,
    top_k: int = 5,
    store: Optional[VectorStore] = None,
    api_key: Optional[str] = None,
):
    """
    Streaming version of ask(). Yields text chunks as they arrive.
    Returns the full response text when complete.
    """
    import anthropic

    if store is None:
        store = build_store()

    results = retrieve(question, store, top_k=top_k)

    context_parts = []
    for r in results:
        context_parts.append(
            f"[Source: {r.chunk.source} | Topic: {r.chunk.topic}]\n{r.chunk.text}"
        )
    context_block = "\n\n---\n\n".join(context_parts)

    knowledge_message = (
        "RELEVANT HVAC KNOWLEDGE (retrieved for this query):\n\n"
        + context_block
    )

    client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    with client.messages.stream(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": knowledge_message,
                        "cache_control": {"type": "ephemeral"},
                    },
                    {
                        "type": "text",
                        "text": f"\nQuestion: {question}",
                    },
                ],
            }
        ],
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
    ) as stream:
        for text in stream.text_stream:
            yield text


# ---------------------------------------------------------------------------
# CLI helper
# ---------------------------------------------------------------------------

def print_retrieved(results: list[RetrievedChunk]) -> None:
    print(f"\n{'='*60}")
    print("RETRIEVED KNOWLEDGE CHUNKS")
    print(f"{'='*60}")
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] {r.chunk.topic}  (score: {r.score:.3f})")
        print(f"    Source: {r.chunk.source} | Tags: {', '.join(r.chunk.tags)}")
        preview = r.chunk.text[:200].replace("\n", " ")
        print(f"    {preview}...")
    print()
