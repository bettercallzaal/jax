"""
HVAC data analysis — trend analysis, anomaly detection, energy calculations.
"""

from typing import Optional
from .psychrometrics import (
    sensible_heat_btuh, coil_capacity_btuh, discharge_temp_expected,
    enthalpy_btu_per_lb, total_heat_btuh,
)


# ---------------------------------------------------------------------------
# Current situation analysis
# ---------------------------------------------------------------------------

def analyze_warm_room_reheat(
    zone: str = "Unknown Zone",
    room_temp_f: float = 0,
    setpoint_f: float = 72,
    discharge_temp_f: float = 85,
    reheat_output_pct: float = 0,
    supply_cfm: Optional[float] = None,
    mixed_air_temp_f: Optional[float] = None,
    hot_water_supply_f: Optional[float] = None,
    hot_water_return_f: Optional[float] = None,
    reheat_type: str = "hot_water",
) -> dict:
    """
    Full analysis of the warm-room / stuck-reheat scenario.
    Returns a structured report dict.
    """
    report = {
        "zone": zone,
        "symptom_summary": [],
        "energy_analysis": {},
        "valve_assessment": {},
        "recommendations": [],
    }

    # --- Symptom summary ---
    if discharge_temp_f > 80 and reheat_output_pct <= 5:
        report["symptom_summary"].append(
            f"Discharge air {discharge_temp_f}°F with {reheat_output_pct}% reheat — "
            "classic stuck-open or leaking valve signature"
        )

    if room_temp_f and room_temp_f > setpoint_f + 2:
        report["symptom_summary"].append(
            f"Room is {room_temp_f - setpoint_f:.1f}°F above setpoint "
            f"({room_temp_f}°F vs {setpoint_f}°F)"
        )

    # --- Energy waste estimate ---
    if supply_cfm and mixed_air_temp_f:
        unwanted_heat = sensible_heat_btuh(supply_cfm, discharge_temp_f - mixed_air_temp_f)
        report["energy_analysis"]["unwanted_reheat_btuh"] = round(unwanted_heat, 0)
        report["energy_analysis"]["unwanted_reheat_tons"] = round(unwanted_heat / 12000, 2)
        # Annualized waste — assume 3000 hrs/yr heating season rough estimate
        annual_kwh = unwanted_heat * 3000 / 3412
        report["energy_analysis"]["est_annual_waste_kwh"] = round(annual_kwh, 0)
        report["symptom_summary"].append(
            f"Estimated unwanted heat: {unwanted_heat:,.0f} BTU/hr "
            f"({unwanted_heat/12000:.2f} tons equivalent)"
        )

    if hot_water_supply_f and hot_water_return_f:
        coil_heat = coil_capacity_btuh(1.0, hot_water_supply_f, hot_water_return_f)
        report["energy_analysis"]["coil_heat_per_gpm_btuh"] = round(coil_heat, 0)
        delta_t = hot_water_supply_f - hot_water_return_f
        report["valve_assessment"]["hw_delta_t_f"] = round(delta_t, 1)
        if delta_t > 5:
            report["valve_assessment"]["interpretation"] = (
                f"HW ΔT of {delta_t:.0f}°F confirms flow through coil — "
                "valve is NOT fully closed"
            )
        else:
            report["valve_assessment"]["interpretation"] = (
                f"HW ΔT near zero ({delta_t:.0f}°F) — minimal or no flow through coil"
            )

    # --- Recommendations ---
    if discharge_temp_f > 80 and reheat_output_pct <= 5 and reheat_type == "hot_water":
        report["recommendations"] = [
            "PRIORITY 1: Verify hot water valve is not stuck open",
            "  - Measure HW supply and return pipe temps at coil",
            "  - Command valve to 0% from DDC, confirm pipe temps change",
            "  - If valve doesn't respond: replace actuator (check actuator type: 2–10VDC, on/off, or floating)",
            "PRIORITY 2: Check DDC controller output",
            "  - Measure output signal at terminal strip with multimeter",
            "  - Typical: 2–10VDC or 4–20mA; 0%=2V or 4mA, 100%=10V or 20mA",
            "PRIORITY 3: Verify fail-safe position",
            "  - Reheat valves should FAIL CLOSED (power-close) to prevent overheating",
            "  - If spring-return: spring should close valve on power loss",
        ]

    return report


def print_analysis_report(report: dict) -> None:
    print(f"\n{'='*60}")
    print(f"HVAC ANALYSIS REPORT — Zone: {report['zone']}")
    print(f"{'='*60}")

    print("\nSYMPTOMS:")
    for s in report["symptom_summary"]:
        print(f"  • {s}")

    if report["energy_analysis"]:
        print("\nENERGY ANALYSIS:")
        for k, v in report["energy_analysis"].items():
            print(f"  {k.replace('_', ' ').title()}: {v}")

    if report["valve_assessment"]:
        print("\nVALVE ASSESSMENT:")
        for k, v in report["valve_assessment"].items():
            print(f"  {k.replace('_', ' ').title()}: {v}")

    if report["recommendations"]:
        print("\nRECOMMENDATIONS:")
        for r in report["recommendations"]:
            print(f"  {r}")

    print()


# ---------------------------------------------------------------------------
# Trend analysis from journal data
# ---------------------------------------------------------------------------

def analyze_trends(journal_entries: list, zone: Optional[str] = None) -> dict:
    """Analyze temperature trends from journal reading entries."""
    readings = [
        e for e in journal_entries
        if e["kind"] == "reading"
        and (zone is None or e.get("zone") == zone)
    ]

    if not readings:
        return {"error": "No reading entries found"}

    # Extract discharge temps over time
    discharge_temps = []
    for r in readings:
        rd = r.get("readings", {})
        for key in ("discharge_temp_f", "discharge_temp", "sat_f", "dat_f"):
            if key in rd:
                discharge_temps.append((r["ts"], float(rd[key])))
                break

    result = {"zone": zone, "reading_count": len(readings)}

    if discharge_temps:
        temps = [t for _, t in discharge_temps]
        result["discharge_temp"] = {
            "min": min(temps),
            "max": max(temps),
            "avg": round(sum(temps) / len(temps), 1),
            "latest": temps[-1],
            "trend": "rising" if temps[-1] > temps[0] else "falling" if temps[-1] < temps[0] else "stable",
        }

    return result
