"""
HVAC diagnostic decision trees and fault analysis.
Based on ASHRAE guidelines and standard field troubleshooting practice.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class Severity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Finding:
    code: str
    description: str
    severity: Severity
    likely_causes: list[str]
    next_steps: list[str]
    notes: str = ""


# ---------------------------------------------------------------------------
# Reheat diagnostics
# ---------------------------------------------------------------------------

def diagnose_reheat(
    discharge_temp_f: float,
    reheat_output_pct: float,
    supply_air_temp_f: Optional[float] = None,
    hot_water_supply_f: Optional[float] = None,
    hot_water_return_f: Optional[float] = None,
    control_signal_pct: Optional[float] = None,
    reheat_type: str = "hot_water",  # "hot_water" | "electric"
) -> list[Finding]:
    """
    Diagnose reheat system faults from field readings.

    The classic symptom: discharge air is warm (85°F+) but reheat output shows 0%.
    This points to heat source entering the coil that the controls don't command.
    """
    findings = []

    # --- Fault 1: Hot discharge with zero reheat output ---
    if discharge_temp_f >= 80 and reheat_output_pct <= 5:
        if reheat_type == "hot_water":
            findings.append(Finding(
                code="RHT-001",
                description="High discharge temp with zero reheat command — coil leaking heat",
                severity=Severity.HIGH,
                likely_causes=[
                    "Hot water valve stuck open or failed open (most common)",
                    "Valve actuator failed or disconnected — valve defaulting open",
                    "Valve bypass/manual override left open",
                    "Balancing valve set too high — residual heat transfer even 'closed'",
                    "Wrong valve fail-safe: valve should fail-closed on reheat, not fail-open",
                    "Control signal wiring shorted — always commanding open",
                    "DDC controller output card failed — stuck at high voltage",
                ],
                next_steps=[
                    "1. Feel HW supply and return pipes at coil — both hot = valve leaking",
                    "2. Command valve to 0% from BAS/controller, measure pipe temps again",
                    "3. Physically inspect valve actuator for disconnection or damage",
                    "4. Check DDC output signal with multimeter (typical: 2–10 VDC or 4–20 mA)",
                    "5. If signal is correct but valve doesn't move → replace actuator",
                    "6. If signal is wrong → trace to DDC output card",
                    "7. Close upstream manual isolation valve to confirm coil source of heat",
                ],
                notes="Confirm by closing manual isolation valve — if discharge drops, valve/coil is the heat source.",
            ))
        elif reheat_type == "electric":
            findings.append(Finding(
                code="RHT-002",
                description="High discharge temp with zero electric reheat command — contactor or SCR stuck closed",
                severity=Severity.HIGH,
                likely_causes=[
                    "Contactor welded closed (failed energized)",
                    "SCR (silicon controlled rectifier) failed in 'on' state",
                    "High-limit thermostat or safety relay bypassed",
                    "Wiring fault — always energizing heating element",
                ],
                next_steps=[
                    "1. De-energize panel — check if discharge temp drops",
                    "2. Measure voltage across heating element with AHU running",
                    "3. Inspect contactors for welding/pitting",
                    "4. Check SCR control board for burn marks",
                    "5. Verify high-limit thermostat is not bypassed",
                ],
            ))

    # --- Fault 2: Reheat commanded but no temperature rise ---
    if reheat_output_pct >= 80 and supply_air_temp_f and discharge_temp_f:
        delta = discharge_temp_f - supply_air_temp_f
        if delta < 5:
            findings.append(Finding(
                code="RHT-003",
                description="Reheat at full command but no temperature rise across coil",
                severity=Severity.HIGH,
                likely_causes=[
                    "Hot water valve stuck closed or actuator failed-closed",
                    "No hot water supply to system (plant off, pump down, valve isolated)",
                    "Hot water supply temp too low (boiler setpoint, mixing valve issue)",
                    "Coil fouled/clogged — restricted flow",
                    "Air trapped in coil (needs purging)",
                    "Electric: heating element failed open, breaker tripped, fuse blown",
                ],
                next_steps=[
                    "1. Verify hot water plant is running and supply temp (should be 120–180°F)",
                    "2. Check valve actuator — command 100%, physically verify valve shaft rotates",
                    "3. Measure HW supply/return pipe temps — if both same = no flow through coil",
                    "4. Open air bleed on coil if present",
                    "5. Check upstream/downstream isolation valves are open",
                    "6. Electric: check breaker, fuse, and element continuity with multimeter",
                ],
            ))

    # --- Fault 3: Hot water supply temperature too low ---
    if hot_water_supply_f and hot_water_supply_f < 100:
        findings.append(Finding(
            code="HWS-001",
            description=f"Hot water supply temp low ({hot_water_supply_f:.0f}°F)",
            severity=Severity.MEDIUM,
            likely_causes=[
                "Boiler setpoint too low or boiler fault",
                "Outdoor air reset driving supply temp down",
                "Mixing valve (3-way) set wrong",
                "Heat exchanger fouled",
                "High system demand — not enough capacity",
            ],
            next_steps=[
                "Check boiler plant status and setpoint",
                "Review OAR (outdoor air reset) schedule — may be appropriate",
                "Verify mixing valve position and setpoint",
            ],
        ))

    # --- Fault 4: High delta-T on hot water coil (restricted flow) ---
    if hot_water_supply_f and hot_water_return_f:
        delta_t = hot_water_supply_f - hot_water_return_f
        if delta_t > 30:
            findings.append(Finding(
                code="HWS-002",
                description=f"Hot water coil ΔT too high ({delta_t:.0f}°F) — restricted flow",
                severity=Severity.MEDIUM,
                likely_causes=[
                    "Coil partially fouled or clogged",
                    "Valve not fully opening",
                    "System pump issue — low flow",
                    "Strainer clogged on coil supply",
                ],
                next_steps=[
                    "Check coil strainer — clean if dirty",
                    "Verify pump operation and flow rates",
                    "Command valve to 100% and re-measure",
                ],
            ))
        elif delta_t < 5 and reheat_output_pct and reheat_output_pct > 50:
            findings.append(Finding(
                code="HWS-003",
                description=f"Hot water coil ΔT near zero ({delta_t:.0f}°F) with reheat commanded — no flow through coil",
                severity=Severity.HIGH,
                likely_causes=[
                    "Valve stuck closed",
                    "Isolation valves closed",
                    "System pump not running",
                    "Coil completely blocked",
                ],
                next_steps=[
                    "Verify pump status",
                    "Check all isolation valves are open",
                    "Command valve open and verify actuator movement",
                ],
            ))

    # --- Fault 5: Control signal vs. valve position mismatch ---
    if control_signal_pct is not None and reheat_output_pct is not None:
        delta = abs(control_signal_pct - reheat_output_pct)
        if delta > 15:
            findings.append(Finding(
                code="CTL-001",
                description=f"Control signal ({control_signal_pct:.0f}%) vs. output ({reheat_output_pct:.0f}%) mismatch",
                severity=Severity.MEDIUM,
                likely_causes=[
                    "Actuator not responding to signal",
                    "Signal wiring issue",
                    "DDC point misconfigured (wrong range, wrong type)",
                    "Actuator needs calibration",
                ],
                next_steps=[
                    "Measure signal at actuator terminals with multimeter",
                    "Verify DDC output range matches actuator input range",
                    "Check for loose terminals or corroded connections",
                ],
            ))

    if not findings:
        findings.append(Finding(
            code="OK-000",
            description="No faults detected from provided readings",
            severity=Severity.INFO,
            likely_causes=[],
            next_steps=["Continue monitoring; collect additional readings for deeper analysis"],
        ))

    return findings


# ---------------------------------------------------------------------------
# Radiation / zone valve diagnostics
# ---------------------------------------------------------------------------

def diagnose_radiation_valve(
    room_temp_f: float,
    setpoint_f: float,
    valve_position_pct: Optional[float] = None,
    valve_type: str = "2way",  # "2way" | "3way" | "zone"
    hand_valved: bool = False,
) -> list[Finding]:
    findings = []

    if hand_valved:
        findings.append(Finding(
            code="RAD-000",
            description="Radiation valve manually isolated (hand-valved off)",
            severity=Severity.INFO,
            likely_causes=["Manual isolation as temporary measure"],
            next_steps=[
                "Replace automatic valve",
                "Restore hand valve to normal position after replacement",
                "Verify room temp stabilizes after replacement",
            ],
        ))

    if room_temp_f > setpoint_f + 3:
        findings.append(Finding(
            code="RAD-001",
            description=f"Room too warm: {room_temp_f:.0f}°F vs setpoint {setpoint_f:.0f}°F",
            severity=Severity.HIGH if room_temp_f > setpoint_f + 8 else Severity.MEDIUM,
            likely_causes=[
                "Radiation valve stuck open — always allowing hot water flow",
                "Valve actuator failed open (common failure mode on spring-return actuators)",
                "Manual valve left open",
                "Incorrect valve fail-safe — should fail closed for heating valve",
                "Thermostat/sensor faulty — reporting wrong room temp",
                "Room sensor in direct sunlight or near heat source",
                "DDC point offset or calibration error",
            ],
            next_steps=[
                "1. Verify room sensor reading with calibrated thermometer",
                "2. Check DDC: what is the zone valve command?",
                "3. If commanded closed but valve is hot → valve stuck open, replace",
                "4. If not commanded → check thermostat/sensor and control logic",
                "5. Hand-valve off as temporary measure while ordering parts",
            ],
        ))
    elif room_temp_f < setpoint_f - 3:
        findings.append(Finding(
            code="RAD-002",
            description=f"Room too cold: {room_temp_f:.0f}°F vs setpoint {setpoint_f:.0f}°F",
            severity=Severity.MEDIUM,
            likely_causes=[
                "Radiation valve stuck closed",
                "No hot water supply to system",
                "Actuator failed closed",
                "DDC not commanding valve open",
                "Incorrect schedule — system in unoccupied setback",
            ],
            next_steps=[
                "Check DDC: is valve being commanded open?",
                "Verify hot water supply is on and at temperature",
                "Check actuator — manually command to open",
                "Inspect for mechanical binding on valve stem",
            ],
        ))

    return findings


# ---------------------------------------------------------------------------
# Room / zone comfort diagnostics
# ---------------------------------------------------------------------------

def diagnose_zone(
    zone: str,
    room_temp_f: float,
    setpoint_f: float,
    discharge_temp_f: Optional[float] = None,
    supply_cfm: Optional[float] = None,
    design_cfm: Optional[float] = None,
    co2_ppm: Optional[float] = None,
    relative_humidity_pct: Optional[float] = None,
) -> list[Finding]:
    findings = []

    # Temperature comfort
    if abs(room_temp_f - setpoint_f) > 3:
        sev = Severity.HIGH if abs(room_temp_f - setpoint_f) > 6 else Severity.MEDIUM
        direction = "warm" if room_temp_f > setpoint_f else "cold"
        findings.append(Finding(
            code="ZN-001",
            description=f"Zone '{zone}' comfort complaint — room {direction}: {room_temp_f:.1f}°F vs {setpoint_f:.1f}°F setpoint",
            severity=sev,
            likely_causes=[
                f"{'Heating' if direction == 'warm' else 'Cooling'} system fault",
                "Sensor error or offset",
                "High internal loads (equipment, occupants)",
                "Envelope/insulation issue",
                "Adjacent zone cross-talk",
            ],
            next_steps=[
                "Verify sensor with independent thermometer",
                "Check zone valve/damper command vs. position",
                "Review recent setpoint changes",
            ],
        ))

    # Airflow
    if supply_cfm and design_cfm:
        ratio = supply_cfm / design_cfm
        if ratio < 0.7:
            findings.append(Finding(
                code="ZN-002",
                description=f"Low airflow: {supply_cfm:.0f} CFM vs design {design_cfm:.0f} CFM ({ratio*100:.0f}%)",
                severity=Severity.MEDIUM,
                likely_causes=[
                    "VAV box stuck at minimum",
                    "Duct obstruction or disconnected duct",
                    "Low AHU static pressure",
                    "Dirty filters — high resistance",
                    "VAV actuator failed",
                ],
                next_steps=[
                    "Measure static pressure at AHU and at zone branch",
                    "Inspect VAV box actuator and damper blade",
                    "Check filter pressure drop",
                    "Verify AHU fan speed/VFD setpoint",
                ],
            ))

    # CO2 / ventilation
    if co2_ppm and co2_ppm > 1100:
        sev = Severity.HIGH if co2_ppm > 1500 else Severity.MEDIUM
        findings.append(Finding(
            code="ZN-003",
            description=f"High CO2: {co2_ppm:.0f} ppm — inadequate ventilation (ASHRAE 62.1 limit ~1100 ppm)",
            severity=sev,
            likely_causes=[
                "Insufficient outside air",
                "DCV (demand control ventilation) not functioning",
                "CO2 sensor fault",
                "High occupancy beyond design",
                "OA damper stuck closed",
            ],
            next_steps=[
                "Check OA damper position and command",
                "Verify CO2 sensor calibration",
                "Review minimum OA setpoints in DDC",
                "Consider manual OA override to increase ventilation",
            ],
        ))

    # Humidity
    if relative_humidity_pct:
        if relative_humidity_pct > 65:
            findings.append(Finding(
                code="ZN-004",
                description=f"High humidity: {relative_humidity_pct:.0f}% RH — mold risk above 65%",
                severity=Severity.HIGH,
                likely_causes=[
                    "Cooling coil leaving air too warm — not dehumidifying",
                    "Overcooled space (thermostat satisfied before dehumidification)",
                    "No mechanical dehumidification",
                    "Infiltration from high-humidity source",
                ],
                next_steps=[
                    "Check cooling coil supply air temp and dew point",
                    "Verify chilled water supply temp is low enough for dehumidification (typically ≤48°F SAT)",
                    "Check for envelope infiltration or plumbing leaks",
                ],
            ))
        elif relative_humidity_pct < 20:
            findings.append(Finding(
                code="ZN-005",
                description=f"Low humidity: {relative_humidity_pct:.0f}% RH — comfort/static issues below 20%",
                severity=Severity.LOW,
                likely_causes=[
                    "No humidification or humidifier off",
                    "High OA fraction in winter without humidity control",
                ],
                next_steps=[
                    "Check humidifier status and setpoint",
                    "Verify OA fraction and preheat coil operation",
                ],
            ))

    return findings


# ---------------------------------------------------------------------------
# Pretty print
# ---------------------------------------------------------------------------

def print_findings(findings: list[Finding]) -> None:
    sev_colors = {
        Severity.INFO: "",
        Severity.LOW: "",
        Severity.MEDIUM: "⚠ ",
        Severity.HIGH: "🔴 ",
        Severity.CRITICAL: "🚨 ",
    }
    for f in findings:
        icon = sev_colors[f.severity]
        print(f"\n{icon}[{f.severity.value}] {f.code}: {f.description}")
        if f.likely_causes:
            print("  Likely causes:")
            for c in f.likely_causes:
                print(f"    • {c}")
        if f.next_steps:
            print("  Next steps:")
            for s in f.next_steps:
                print(f"    → {s}")
        if f.notes:
            print(f"  Note: {f.notes}")
