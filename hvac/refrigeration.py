"""
Refrigeration cycle diagnostics — superheat, subcooling, P-T tables.
Supports R-410A, R-22, R-32, R-134a.
"""

from dataclasses import dataclass
from typing import Optional
import math


# ---------------------------------------------------------------------------
# Saturation pressure-temperature tables (psia vs °F)
# Interpolated from ASHRAE / NIST data
# ---------------------------------------------------------------------------

# Format: {temp_f: sat_pressure_psia}
R410A_SAT = {
    -40: 14.7, -30: 20.4, -20: 27.8, -10: 37.0, 0: 48.3,
    10: 62.0, 20: 78.5, 30: 98.3, 40: 121.7, 45: 135.0,
    50: 149.4, 55: 165.2, 60: 182.5, 70: 221.3, 80: 265.8,
    90: 316.8, 95: 344.8, 100: 374.2, 105: 405.3, 110: 438.2,
    115: 473.0, 120: 509.7, 130: 589.0, 140: 676.0,
}

R22_SAT = {
    -40: 4.9, -30: 7.4, -20: 10.8, -10: 15.3, 0: 21.1,
    10: 28.4, 20: 37.7, 30: 49.3, 40: 63.6, 50: 80.9,
    60: 101.6, 70: 126.0, 80: 154.4, 90: 187.3, 95: 205.5,
    100: 224.9, 105: 245.6, 110: 267.6, 120: 315.8, 130: 370.0,
}

R32_SAT = {
    -40: 13.0, -30: 18.5, -20: 25.6, -10: 34.7, 0: 45.8,
    10: 59.5, 20: 76.1, 30: 96.0, 40: 119.6, 50: 147.3,
    60: 179.5, 70: 216.8, 80: 259.7, 90: 308.7, 100: 364.2,
    110: 426.8, 120: 497.0, 130: 575.6,
}

R134A_SAT = {
    -40: 7.4, -30: 10.9, -20: 15.8, -10: 22.2, 0: 30.6,
    10: 41.2, 20: 54.4, 30: 70.9, 40: 91.0, 50: 114.9,
    60: 143.1, 70: 176.2, 80: 214.5, 90: 258.6, 100: 308.8,
    110: 365.7, 120: 429.9, 130: 501.8,
}

REFRIGERANT_TABLES = {
    "R410A": R410A_SAT,
    "R22": R22_SAT,
    "R32": R32_SAT,
    "R134A": R134A_SAT,
}

REFRIGERANT_LIMITS = {
    "R410A": {"max_discharge_temp_f": 240, "high_pressure_psia": 400, "low_pressure_psia": 30},
    "R22":   {"max_discharge_temp_f": 240, "high_pressure_psia": 300, "low_pressure_psia": 20},
    "R32":   {"max_discharge_temp_f": 250, "high_pressure_psia": 450, "low_pressure_psia": 35},
    "R134A": {"max_discharge_temp_f": 230, "high_pressure_psia": 250, "low_pressure_psia": 15},
}


def sat_temp_f(pressure_psia: float, refrigerant: str = "R410A") -> float:
    """Interpolate saturation temperature (°F) from pressure (psia)."""
    table = REFRIGERANT_TABLES.get(refrigerant.upper())
    if not table:
        raise ValueError(f"Unknown refrigerant: {refrigerant}. Supported: {list(REFRIGERANT_TABLES)}")
    sorted_items = sorted(table.items(), key=lambda x: x[0])  # sorted by temp
    # Build reverse lookup: pressure → temp
    temps = [t for t, _ in sorted_items]
    pressures = [p for _, p in sorted_items]
    if pressure_psia <= pressures[0]:
        return temps[0]
    if pressure_psia >= pressures[-1]:
        return temps[-1]
    for i in range(len(pressures) - 1):
        if pressures[i] <= pressure_psia <= pressures[i + 1]:
            ratio = (pressure_psia - pressures[i]) / (pressures[i + 1] - pressures[i])
            return temps[i] + ratio * (temps[i + 1] - temps[i])
    return temps[-1]


def sat_pressure_psia(temp_f: float, refrigerant: str = "R410A") -> float:
    """Interpolate saturation pressure (psia) from temperature (°F)."""
    table = REFRIGERANT_TABLES.get(refrigerant.upper())
    if not table:
        raise ValueError(f"Unknown refrigerant: {refrigerant}")
    sorted_items = sorted(table.items())
    temps = [t for t, _ in sorted_items]
    pressures = [p for _, p in sorted_items]
    if temp_f <= temps[0]:
        return pressures[0]
    if temp_f >= temps[-1]:
        return pressures[-1]
    for i in range(len(temps) - 1):
        if temps[i] <= temp_f <= temps[i + 1]:
            ratio = (temp_f - temps[i]) / (temps[i + 1] - temps[i])
            return pressures[i] + ratio * (pressures[i + 1] - pressures[i])
    return pressures[-1]


# ---------------------------------------------------------------------------
# Superheat & Subcooling
# ---------------------------------------------------------------------------

def superheat(suction_temp_f: float, suction_pressure_psia: float,
              refrigerant: str = "R410A") -> float:
    """Superheat = suction line temp - saturation temp at suction pressure."""
    t_sat = sat_temp_f(suction_pressure_psia, refrigerant)
    return suction_temp_f - t_sat


def subcooling(liquid_temp_f: float, condensing_pressure_psia: float,
               refrigerant: str = "R410A") -> float:
    """Subcooling = saturation temp at condensing pressure - liquid line temp."""
    t_sat = sat_temp_f(condensing_pressure_psia, refrigerant)
    return t_sat - liquid_temp_f


@dataclass
class RefrigerantState:
    superheat_f: float
    subcooling_f: float
    suction_sat_temp_f: float
    discharge_sat_temp_f: float
    compression_ratio: float
    diagnosis: list[str]
    severity: str  # "ok" | "warning" | "fault"


def analyze_refrigerant(
    suction_temp_f: float,
    suction_pressure_psia: float,
    discharge_temp_f: float,
    discharge_pressure_psia: float,
    liquid_temp_f: float,
    refrigerant: str = "R410A",
    target_superheat_f: float = 12.0,
    target_subcooling_f: float = 7.0,
) -> RefrigerantState:
    """Full refrigerant circuit analysis."""
    sh = superheat(suction_temp_f, suction_pressure_psia, refrigerant)
    sc = subcooling(liquid_temp_f, discharge_pressure_psia, refrigerant)
    suction_sat = sat_temp_f(suction_pressure_psia, refrigerant)
    discharge_sat = sat_temp_f(discharge_pressure_psia, refrigerant)
    comp_ratio = discharge_pressure_psia / suction_pressure_psia

    limits = REFRIGERANT_LIMITS.get(refrigerant.upper(), {})
    diagnosis = []
    severity = "ok"

    # Superheat analysis
    if sh < 5:
        diagnosis.append(f"LOW SUPERHEAT ({sh:.1f}°F < 5°F): Risk of liquid slugging compressor. Check TXV/EEV, check for overcharge.")
        severity = "fault"
    elif sh < target_superheat_f - 3:
        diagnosis.append(f"Superheat slightly low ({sh:.1f}°F): May be slightly overcharged or TXV set too open.")
        severity = "warning" if severity == "ok" else severity
    elif sh > 25:
        diagnosis.append(f"HIGH SUPERHEAT ({sh:.1f}°F > 25°F): System undercharged or TXV too restrictive. Reduced capacity.")
        severity = "fault"
    elif sh > target_superheat_f + 5:
        diagnosis.append(f"Superheat elevated ({sh:.1f}°F): Possibly low refrigerant charge or TXV hunting.")
        severity = "warning" if severity == "ok" else severity
    else:
        diagnosis.append(f"Superheat OK ({sh:.1f}°F — target {target_superheat_f}°F)")

    # Subcooling analysis
    if sc < 3:
        diagnosis.append(f"LOW SUBCOOLING ({sc:.1f}°F < 3°F): Risk of flash gas at expansion device. Check for low charge or liquid line restriction.")
        severity = "fault"
    elif sc > 15:
        diagnosis.append(f"HIGH SUBCOOLING ({sc:.1f}°F > 15°F): System may be overcharged. Verify condenser performance.")
        severity = "warning" if severity == "ok" else severity
    else:
        diagnosis.append(f"Subcooling OK ({sc:.1f}°F — target {target_subcooling_f}°F)")

    # Discharge temperature
    max_disc = limits.get("max_discharge_temp_f", 240)
    if discharge_temp_f > max_disc:
        diagnosis.append(f"DISCHARGE TEMP CRITICAL ({discharge_temp_f:.0f}°F > {max_disc}°F): Compressor at risk. Check charge, condenser, oil.")
        severity = "fault"
    elif discharge_temp_f > max_disc - 20:
        diagnosis.append(f"Discharge temp elevated ({discharge_temp_f:.0f}°F): Monitor closely.")
        severity = "warning" if severity == "ok" else severity

    # Compression ratio
    if comp_ratio > 10:
        diagnosis.append(f"HIGH COMPRESSION RATIO ({comp_ratio:.1f}): Low suction or high discharge pressure. Check for low charge + high ambient.")
        severity = "fault"
    elif comp_ratio > 8:
        diagnosis.append(f"Compression ratio elevated ({comp_ratio:.1f}): Investigate condenser performance or charge.")
        severity = "warning" if severity == "ok" else severity

    # High-pressure fault
    hp_limit = limits.get("high_pressure_psia", 400)
    if discharge_pressure_psia > hp_limit:
        diagnosis.append(f"DISCHARGE PRESSURE OVER LIMIT ({discharge_pressure_psia:.0f} > {hp_limit} psia): High-pressure switch should trip. Check condenser.")
        severity = "fault"

    return RefrigerantState(
        superheat_f=round(sh, 1),
        subcooling_f=round(sc, 1),
        suction_sat_temp_f=round(suction_sat, 1),
        discharge_sat_temp_f=round(discharge_sat, 1),
        compression_ratio=round(comp_ratio, 2),
        diagnosis=diagnosis,
        severity=severity,
    )


def print_refrigerant_state(state: RefrigerantState, refrigerant: str = "R410A") -> None:
    sev_icon = {"ok": "✓", "warning": "⚠", "fault": "🔴"}.get(state.severity, "?")
    print(f"\n{'='*55}")
    print(f"REFRIGERANT ANALYSIS ({refrigerant})  {sev_icon} {state.severity.upper()}")
    print(f"{'='*55}")
    print(f"  Superheat        : {state.superheat_f:.1f} °F")
    print(f"  Subcooling       : {state.subcooling_f:.1f} °F")
    print(f"  Suction Sat Temp : {state.suction_sat_temp_f:.1f} °F")
    print(f"  Condensing Temp  : {state.discharge_sat_temp_f:.1f} °F")
    print(f"  Compression Ratio: {state.compression_ratio:.2f}:1")
    print(f"\nDiagnosis:")
    for d in state.diagnosis:
        print(f"  • {d}")
    print()
