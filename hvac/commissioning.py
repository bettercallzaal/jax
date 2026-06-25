"""
HVAC commissioning checklists and startup procedures.
Based on ASHRAE Guideline 1.1 and standard field practice.
"""

from dataclasses import dataclass, field
from typing import Optional
from .journal import log_action


@dataclass
class ChecklistItem:
    id: str
    description: str
    category: str
    critical: bool = False
    passed: Optional[bool] = None
    notes: str = ""


def pre_startup_checklist() -> list[ChecklistItem]:
    """Full pre-startup mechanical, electrical, and controls checklist."""
    return [
        # --- Mechanical ---
        ChecklistItem("M01", "All ductwork connections tight and sealed (no visible gaps)", "Mechanical", critical=True),
        ChecklistItem("M02", "Equipment mounting bolts torqued to spec", "Mechanical"),
        ChecklistItem("M03", "Vibration isolators installed and equally compressed", "Mechanical"),
        ChecklistItem("M04", "Refrigerant lines: no kinks, insulation intact, proper slope", "Mechanical", critical=True),
        ChecklistItem("M05", "Control valves installed in correct flow direction (arrow visible)", "Mechanical", critical=True),
        ChecklistItem("M06", "Filters installed with correct airflow direction", "Mechanical", critical=True),
        ChecklistItem("M07", "All access panels closed and secured", "Mechanical"),
        ChecklistItem("M08", "Outdoor unit clear of obstructions (≥3 ft clearance)", "Mechanical"),
        ChecklistItem("M09", "Drain pan clean and drain line clear", "Mechanical"),
        ChecklistItem("M10", "Coil fins straight (straighten if bent)", "Mechanical"),

        # --- Electrical ---
        ChecklistItem("E01", "Breaker amperage matches equipment nameplate (within ±10%)", "Electrical", critical=True),
        ChecklistItem("E02", "Voltage at equipment matches nameplate", "Electrical", critical=True),
        ChecklistItem("E03", "Ground and neutral properly bonded", "Electrical", critical=True),
        ChecklistItem("E04", "3-phase rotation correct (verified with phase rotation meter)", "Electrical"),
        ChecklistItem("E05", "Control wiring complete, shielded for sensor cables", "Electrical"),
        ChecklistItem("E06", "24V transformer installed and fused", "Electrical"),
        ChecklistItem("E07", "Thermostat/sensor wiring identified and labeled", "Electrical"),
        ChecklistItem("E08", "Motor capacitors correct rating (run/start)", "Electrical"),

        # --- Hydronic ---
        ChecklistItem("H01", "System filled to proper pressure (typically 1–2 bar / 15–30 psi)", "Hydronic", critical=True),
        ChecklistItem("H02", "Air purged from system (manual bleeder valves opened at high points)", "Hydronic", critical=True),
        ChecklistItem("H03", "Pump rotation correct (no cavitation)", "Hydronic", critical=True),
        ChecklistItem("H04", "Expansion tank pre-charge set for system pressure", "Hydronic"),
        ChecklistItem("H05", "All isolation valves open (supply and return)", "Hydronic", critical=True),
        ChecklistItem("H06", "Strainers clean (record delta-P across strainer)", "Hydronic"),
        ChecklistItem("H07", "Balancing valves at design position", "Hydronic"),
        ChecklistItem("H08", "Flow meter functional (if installed)", "Hydronic"),

        # --- Controls & Sensors ---
        ChecklistItem("C01", "All sensors in place (temperature, humidity, pressure, CO2)", "Controls", critical=True),
        ChecklistItem("C02", "Sensor calibration verified (ice bath / reference thermometer)", "Controls", critical=True),
        ChecklistItem("C03", "DDC controller powered, network connection verified", "Controls", critical=True),
        ChecklistItem("C04", "System time synchronized (for scheduling)", "Controls"),
        ChecklistItem("C05", "Battery backup operational", "Controls"),
        ChecklistItem("C06", "All DDC outputs functional (test each analog and binary output)", "Controls", critical=True),
        ChecklistItem("C07", "Setpoints documented and entered in BAS", "Controls"),
        ChecklistItem("C08", "Occupied/unoccupied schedule verified", "Controls"),
        ChecklistItem("C09", "High-limit safeties functional (simulate and verify shutdown)", "Controls", critical=True),
        ChecklistItem("C10", "Economizer damper operation verified (if applicable)", "Controls"),
    ]


def startup_sequence() -> list[dict]:
    """Step-by-step startup sequence with expected observations."""
    return [
        {
            "step": 1,
            "title": "Blower Only (No Heating/Cooling)",
            "duration_min": 15,
            "actions": [
                "Start supply fan only (disable heating and cooling stages)",
                "Listen for rubbing, grinding, or bearing noise",
                "Verify airflow at all supply and return grilles",
                "Check for ductwork vibration or rattles",
                "Measure filter pressure drop (clean: 0.1–0.2\" WC max)",
            ],
            "pass_criteria": [
                "No unusual mechanical noise",
                "Air movement confirmed at all outlets",
                "Filter ΔP < 0.3\" WC",
            ],
        },
        {
            "step": 2,
            "title": "Cooling Stage Startup",
            "duration_min": 20,
            "actions": [
                "Enable mechanical cooling",
                "Monitor discharge pressure — should build gradually (not spike)",
                "Verify evaporator/coil outlet temperature drops within 2 minutes",
                "Check suction pressure stabilizes (should not fluctuate > 10 psi)",
                "Measure supply air temperature delta (ΔT = 15–20°F typical)",
                "Verify condensate drain flowing (if dehumidifying)",
            ],
            "pass_criteria": [
                "Supply air temp drops to setpoint (typically 55°F)",
                "Suction pressure stable",
                "Superheat 8–15°F (if refrigerant system)",
                "No high-pressure fault",
            ],
        },
        {
            "step": 3,
            "title": "Heating Stage Startup",
            "duration_min": 20,
            "actions": [
                "Enable heating, disable cooling",
                "Hot water: Verify pump running and HW supply/return temps rise",
                "Electric: Monitor current draw vs. nameplate amperage",
                "Gas: Verify flame sensor, no flame rollout",
                "Measure discharge temperature rise (ΔT = 20–40°F typical)",
            ],
            "pass_criteria": [
                "Discharge temp rises to heating setpoint",
                "HW ΔT across coil: 10–20°F at design flow",
                "No high-limit trips",
                "Modulation smooth (no hunting)",
            ],
        },
        {
            "step": 4,
            "title": "Controls Verification",
            "duration_min": 30,
            "actions": [
                "Raise space setpoint 2°F above current room temp — heating should activate within 2 min",
                "Lower setpoint 2°F below room temp — cooling should activate within 2 min",
                "Verify deadband: No simultaneous heating AND cooling",
                "Test DCV: Blow CO2 source near sensor — OA should increase",
                "Verify economizer lockout at high outdoor humidity (if applicable)",
                "Force high-limit fault — system should shut down and alarm",
            ],
            "pass_criteria": [
                "Heating/cooling respond within 2 minutes of setpoint change",
                "No simultaneous heating+cooling (lockout proven)",
                "Alarms annunciate in BAS",
                "System returns to normal after alarm clear",
            ],
        },
        {
            "step": 5,
            "title": "Airflow Balancing",
            "duration_min": 60,
            "actions": [
                "Measure CFM at each supply diffuser (flow hood or pitot traverse)",
                "Measure static pressure at AHU supply and return plenums",
                "Adjust VAV box and branch dampers to design CFM",
                "Verify return airflow balanced with supply (< 10% difference)",
                "Document all readings on balancing report",
            ],
            "pass_criteria": [
                "Each diffuser within ±10% of design CFM",
                "Supply/return CFM within 10% of each other",
                "No zones over-pressurized or starved",
            ],
        },
    ]


def sensor_calibration_procedure(sensor_type: str = "temperature") -> list[str]:
    """Return field calibration steps for a given sensor type."""
    if sensor_type == "temperature":
        return [
            "ICE BATH METHOD (32°F reference):",
            "  1. Fill container with crushed ice + distilled water (slurry, not just water)",
            "  2. Wait 5–10 minutes for thermal equilibrium",
            "  3. Insert calibrated reference thermometer (±0.5°F) and sensor probe",
            "  4. Hold both vertical, 2–3 inches deep in slurry",
            "  5. Compare readings — adjust if error > ±2°F",
            "  6. Document: technician, date, sensor ID, reading before/after adjustment",
            "",
            "BOILING WATER METHOD (212°F reference at sea level):",
            "  1. Heat water to rolling boil",
            "  2. Insert reference and sensor into steam (not touching water)",
            "  3. Hold 60 seconds, read simultaneously",
            "  4. Adjust if error > ±2°F",
            "  NOTE: Adjust 212°F by -0.5°F per 1000 ft elevation",
        ]
    elif sensor_type == "pressure":
        return [
            "PRESSURE SENSOR CALIBRATION:",
            "  1. Zero sensor at atmospheric pressure (disconnect from system)",
            "  2. Apply test pressures: 25%, 50%, 75%, 100% of sensor range",
            "  3. Use deadweight tester (±0.5%) or calibrated gauge as reference",
            "  4. Record error at each test point",
            "  5. Adjust zero and span if error > ±2% at any point",
            "  6. Verify linearity across full range",
            "  7. Recommended recalibration interval: every 6–12 months",
        ]
    elif sensor_type == "humidity":
        return [
            "HUMIDITY SENSOR CALIBRATION (field verification):",
            "  1. Compare sensor reading to calibrated psychrometer in same air mass",
            "  2. Acceptable field tolerance: ±5% RH",
            "  3. Verify sensor is NOT:",
            "     - In direct sunlight",
            "     - Near a heat source or exhaust",
            "     - In an air jet (should be in well-mixed zone)",
            "  4. If error > ±5%: Send sensor to factory calibration service",
            "  Note: Salt solution method (LiCl = 11.3% RH, NaCl = 75.3% RH) for lab calibration",
        ]
    elif sensor_type == "co2":
        return [
            "CO2 SENSOR CALIBRATION:",
            "  1. Fresh air calibration: Take sensor to outdoor location away from traffic/HVAC exhausts",
            "  2. Wait 5 minutes — outdoor CO2 is approximately 420 ppm (2024 baseline)",
            "  3. Press calibration button (if equipped) or set offset in BAS to read 420 ppm",
            "  4. Verify alarm setpoints: Warning ~1000 ppm, High ~1500 ppm",
            "  5. Recommended recalibration: Annually",
        ]
    return [f"No calibration procedure defined for sensor type: {sensor_type}"]


def run_checklist(checklist: list[ChecklistItem], zone: str = "General") -> dict:
    """Interactively run a checklist (CLI mode)."""
    results = {"passed": 0, "failed": 0, "skipped": 0, "critical_failures": []}
    print(f"\nRunning checklist for zone: {zone}")
    print("=" * 60)
    print("Press ENTER=pass, f=fail, s=skip, then ENTER for notes")
    print("=" * 60)

    for item in checklist:
        crit = " [CRITICAL]" if item.critical else ""
        print(f"\n[{item.id}]{crit} {item.description}")
        response = input("  Result (enter/f/s): ").strip().lower()
        if response == "f":
            item.passed = False
            notes = input("  Notes: ").strip()
            item.notes = notes
            results["failed"] += 1
            if item.critical:
                results["critical_failures"].append(item.id)
            log_action(zone=zone, action=f"Checklist {item.id} FAILED: {item.description}", outcome=notes or "failed")
        elif response == "s":
            item.passed = None
            results["skipped"] += 1
        else:
            item.passed = True
            results["passed"] += 1

    print(f"\n{'='*60}")
    print(f"CHECKLIST COMPLETE — {zone}")
    print(f"  Passed : {results['passed']}")
    print(f"  Failed : {results['failed']}")
    print(f"  Skipped: {results['skipped']}")
    if results["critical_failures"]:
        print(f"  CRITICAL FAILURES: {', '.join(results['critical_failures'])}")
        print("  *** DO NOT START SYSTEM until critical items resolved ***")
    print(f"{'='*60}")
    return results


def print_startup_sequence() -> None:
    """Print the full startup procedure."""
    steps = startup_sequence()
    print("\nHVAC STARTUP SEQUENCE")
    print("=" * 60)
    for step in steps:
        print(f"\nSTEP {step['step']}: {step['title']} (~{step['duration_min']} min)")
        print("  Actions:")
        for a in step["actions"]:
            print(f"    • {a}")
        print("  Pass Criteria:")
        for p in step["pass_criteria"]:
            print(f"    ✓ {p}")
