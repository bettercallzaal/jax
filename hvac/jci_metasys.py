"""
JCI Metasys — point naming conventions, VAV with hot water reheat sequences,
and common troubleshooting paths for Johnson Controls BAS.
"""

# ---------------------------------------------------------------------------
# Standard Metasys point name patterns for VAV boxes with HW reheat
# ---------------------------------------------------------------------------

VAV_POINT_MAP = {
    # Airflow
    "airflow_cfm":         "ZN-T / AHU-VAV-{box}-CFM",
    "damper_position_pct": "ZN-T / AHU-VAV-{box}-DMPR-POS",
    "damper_command_pct":  "ZN-T / AHU-VAV-{box}-DMPR-CMD",
    "min_cfm_setpoint":    "ZN-T / AHU-VAV-{box}-CFM-MIN",
    "max_cfm_setpoint":    "ZN-T / AHU-VAV-{box}-CFM-MAX",
    "design_cfm":          "ZN-T / AHU-VAV-{box}-CFM-DES",

    # Temperature
    "zone_temp_f":         "ZN-T / AHU-VAV-{box}-ZN-T",
    "zone_setpoint_f":     "ZN-T / AHU-VAV-{box}-ZN-SP",
    "discharge_temp_f":    "ZN-T / AHU-VAV-{box}-DAT",
    "supply_air_temp_f":   "AHU-{ahu}-SAT",

    # Reheat valve
    "hw_valve_cmd_pct":    "ZN-T / AHU-VAV-{box}-HW-VLV-CMD",
    "hw_valve_pos_pct":    "ZN-T / AHU-VAV-{box}-HW-VLV-POS",
    "hw_supply_temp_f":    "HW-SUPPLY-T",
    "hw_return_temp_f":    "HW-RETURN-T",

    # Mode
    "zone_mode":           "ZN-T / AHU-VAV-{box}-MODE",
    # Typical values: 0=Unoccupied, 1=Occupied, 2=Standby, 3=Warmup, 4=Cooldown
    "control_mode":        "ZN-T / AHU-VAV-{box}-CTRL-MODE",
    # Typical: 1=Cooling, 2=Deadband, 3=Heating
}

ZONE_MODES = {0: "Unoccupied", 1: "Occupied", 2: "Standby", 3: "Warmup", 4: "Cooldown", 5: "Purge"}
CONTROL_MODES = {1: "Cooling", 2: "Deadband", 3: "Heating"}


# ---------------------------------------------------------------------------
# Typical VAV + HW Reheat sequence of operation (JCI Metasys / NAE/NCE)
# ---------------------------------------------------------------------------

VAV_HW_REHEAT_SEQUENCE = """
VAV BOX WITH HOT WATER REHEAT — Sequence of Operation (JCI Metasys)

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
  - If CFM sensor reading 0 with damper open: Airflow sensor fault
"""

# ---------------------------------------------------------------------------
# Metasys diagnostic checklist: VAV box with HW reheat stuck-open valve
# ---------------------------------------------------------------------------

REHEAT_STUCK_OPEN_CHECKS = [
    {
        "step": 1,
        "action": "Navigate to VAV box object in Metasys Site Director",
        "look_for": "HW-VLV-CMD vs HW-VLV-POS — command should be 0%, check if position matches",
        "note": "In Metasys: Focus → Equipment → VAV-{box} → View",
    },
    {
        "step": 2,
        "action": "Check CTRL-MODE point",
        "look_for": "Should show 'Deadband' or 'Cooling' if zone is warm. If showing 'Heating' — logic is commanding heat.",
        "note": "If CTRL-MODE=Heating with warm room → check zone sensor reading and setpoints",
    },
    {
        "step": 3,
        "action": "Override HW valve to 0% in Metasys (operator override)",
        "look_for": "Watch DAT point — if discharge temp drops within 2–3 minutes, valve was passing flow",
        "note": "Focus → VAV-{box} → HW-VLV-CMD → Override to 0",
    },
    {
        "step": 4,
        "action": "Check override vs. feedback",
        "look_for": "HW-VLV-CMD = 0%, HW-VLV-POS still showing >0? → actuator not responding to signal",
        "note": "Also possible: no position feedback wired — POS always reads same as CMD",
    },
    {
        "step": 5,
        "action": "Go physical: feel HW supply and return pipes at the VAV box coil",
        "look_for": "Both pipes hot with CMD=0% → valve body stuck open or actuator disconnected",
        "note": "Pipe temp delta: Supply - Return should drop to <5°F if valve truly closed",
    },
    {
        "step": 6,
        "action": "Check actuator signal at terminal strip",
        "look_for": "Metasys analog output: 0–10VDC (0%=2V, 100%=10V) or 4–20mA (0%=4mA)",
        "note": "Measure with multimeter. If signal correct but valve doesn't move → replace actuator",
    },
    {
        "step": 7,
        "action": "Clear override in Metasys, verify normal operation resumes",
        "look_for": "Valve should modulate per heating demand, DAT within normal range (55–85°F)",
        "note": "Document findings and override removal time in Metasys activity log",
    },
]

# ---------------------------------------------------------------------------
# Common Metasys fault patterns for VAV+HW reheat
# ---------------------------------------------------------------------------

METASYS_FAULT_PATTERNS = {
    "DAT_HIGH_HW_ZERO": {
        "symptom": "Discharge air temp high (>85°F), HW valve command at 0%",
        "likely_cause": [
            "Valve stuck open / actuator failed — valve leaking hot water regardless of command",
            "Valve wired backwards (0V=open, 10V=closed) — check actuator documentation",
            "DDC output failed HIGH — check controller output module",
        ],
        "metasys_path": "Equipment → VAV-{box} → Points: DAT, HW-VLV-CMD, HW-VLV-POS, CTRL-MODE",
    },
    "ZONE_WARM_VALVE_ZERO_MODE_COOL": {
        "symptom": "Zone warm, HW valve 0%, control mode = Cooling",
        "likely_cause": [
            "Cooling not working or insufficient cooling supply air",
            "Damper not opening — check CFM vs damper command",
            "Supply air temp too high from AHU",
        ],
        "metasys_path": "Equipment → VAV-{box} → DMPR-CMD, CFM, AHU-SAT",
    },
    "DAT_SENSOR_FAULT": {
        "symptom": "DAT reading stuck at fixed value or out of range",
        "likely_cause": [
            "Sensor disconnected or shorted (Metasys will show default/last value)",
            "Sensor location wrong — in dead air pocket or near heat source",
        ],
        "metasys_path": "Points → DAT → Properties → check reliability and last-update timestamp",
    },
    "CFM_ZERO_DAMPER_OPEN": {
        "symptom": "Airflow reads 0 CFM with damper commanded open",
        "likely_cause": [
            "Pitot tube clogged (common in dusty environments)",
            "Differential pressure transducer failed",
            "AHU fan off — no supply air",
            "Damper actuator failed — blade not moving despite command",
        ],
        "metasys_path": "Equipment → VAV-{box} → CFM, DMPR-CMD, DMPR-POS",
    },
}


def print_fault_pattern(pattern_key: str) -> None:
    pattern = METASYS_FAULT_PATTERNS.get(pattern_key)
    if not pattern:
        print(f"Unknown pattern: {pattern_key}. Available: {list(METASYS_FAULT_PATTERNS)}")
        return
    print(f"\nFAULT PATTERN: {pattern_key}")
    print(f"  Symptom     : {pattern['symptom']}")
    print(f"  Metasys Path: {pattern['metasys_path']}")
    print("  Likely Causes:")
    for c in pattern["likely_cause"]:
        print(f"    • {c}")


def print_reheat_diagnostic_steps(box_id: str = "VAV-1") -> None:
    """Print step-by-step Metasys reheat diagnostic for a specific VAV box."""
    print(f"\n{'='*60}")
    print(f"METASYS REHEAT DIAGNOSTIC — {box_id}")
    print(f"System: JCI Metasys | Terminal: VAV+HW Reheat | Fluid: Hot Water")
    print(f"{'='*60}")
    for step in REHEAT_STUCK_OPEN_CHECKS:
        print(f"\nStep {step['step']}: {step['action']}")
        print(f"  Look for: {step['look_for']}")
        print(f"  Note    : {step['note'].replace('{box}', box_id)}")
    print()


def print_sequence() -> None:
    print(VAV_HW_REHEAT_SEQUENCE)
