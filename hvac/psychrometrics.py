"""
Psychrometric calculations for HVAC field analysis.
All temperatures in °F, pressures in psia, unless noted.
"""

import math


# --- Saturation pressure (Antoine equation approximation) ---

def sat_pressure_psia(dry_bulb_f: float) -> float:
    """Saturation vapor pressure at dry bulb temp (°F), returns psia."""
    t = (dry_bulb_f - 32) * 5 / 9  # convert to °C
    # Magnus formula
    p_kpa = 0.6108 * math.exp(17.27 * t / (t + 237.3))
    return p_kpa * 0.145038  # kPa → psia


def humidity_ratio(dry_bulb_f: float, relative_humidity_pct: float,
                   altitude_ft: float = 0) -> float:
    """Humidity ratio W (lb water / lb dry air)."""
    patm = atmospheric_pressure_psia(altitude_ft)
    psat = sat_pressure_psia(dry_bulb_f)
    pw = (relative_humidity_pct / 100) * psat
    return 0.62198 * pw / (patm - pw)


def atmospheric_pressure_psia(altitude_ft: float = 0) -> float:
    """Standard atmospheric pressure at altitude (ft)."""
    # ASHRAE standard atmosphere
    return 14.696 * (1 - 6.8754e-6 * altitude_ft) ** 5.2559


def dew_point_f(dry_bulb_f: float, relative_humidity_pct: float) -> float:
    """Dew point temperature (°F) from dry bulb and RH."""
    t = (dry_bulb_f - 32) * 5 / 9
    rh = relative_humidity_pct
    a = 17.27
    b = 237.3
    alpha = (a * t / (b + t)) + math.log(rh / 100)
    td_c = (b * alpha) / (a - alpha)
    return td_c * 9 / 5 + 32


def wet_bulb_f(dry_bulb_f: float, relative_humidity_pct: float,
               altitude_ft: float = 0) -> float:
    """Wet bulb temperature (°F) — Stull (2011) approximation."""
    t = dry_bulb_f
    rh = relative_humidity_pct
    # Stull formula (works for 5–99% RH, -20 to 50°C)
    tc = (t - 32) * 5 / 9
    twc = (tc * math.atan(0.151977 * (rh + 8.313659) ** 0.5)
           + math.atan(tc + rh)
           - math.atan(rh - 1.676331)
           + 0.00391838 * rh ** 1.5 * math.atan(0.023101 * rh)
           - 4.686035)
    return twc * 9 / 5 + 32


def enthalpy_btu_per_lb(dry_bulb_f: float, relative_humidity_pct: float,
                         altitude_ft: float = 0) -> float:
    """Enthalpy of moist air (BTU / lb dry air)."""
    w = humidity_ratio(dry_bulb_f, relative_humidity_pct, altitude_ft)
    # h = 0.240*T + W*(1061 + 0.444*T)  [ASHRAE]
    return 0.240 * dry_bulb_f + w * (1061 + 0.444 * dry_bulb_f)


def cfm_to_lbs_per_hour(cfm: float, dry_bulb_f: float = 70,
                          altitude_ft: float = 0) -> float:
    """Convert CFM to mass flow rate (lb dry air / hr)."""
    patm_psia = atmospheric_pressure_psia(altitude_ft)
    # Specific volume of dry air (approx)
    t_rankine = dry_bulb_f + 459.67
    v = 0.3704 * t_rankine / (patm_psia * 144)  # ft³/lb
    return cfm * 60 / v


def sensible_heat_btuh(cfm: float, delta_t_f: float) -> float:
    """Sensible heat transfer (BTU/hr). Q = 1.1 * CFM * ΔT (sea level)."""
    return 1.1 * cfm * delta_t_f


def latent_heat_btuh(cfm: float, delta_w: float) -> float:
    """Latent heat transfer (BTU/hr). Q = 4840 * CFM * ΔW."""
    return 4840 * cfm * delta_w


def total_heat_btuh(cfm: float, delta_enthalpy: float) -> float:
    """Total heat transfer (BTU/hr). Q = 4.5 * CFM * Δh."""
    return 4.5 * cfm * delta_enthalpy


def coil_capacity_btuh(gpm: float, supply_temp_f: float,
                        return_temp_f: float) -> float:
    """Hot/chilled water coil capacity (BTU/hr). Q = 500 * GPM * ΔT."""
    return 500 * gpm * abs(supply_temp_f - return_temp_f)


def discharge_temp_expected(mixed_air_f: float, reheat_btuh: float,
                             cfm: float) -> float:
    """Expected discharge air temp given mixed air temp and reheat output."""
    delta_t = reheat_btuh / (1.1 * cfm) if cfm else 0
    return mixed_air_f + delta_t


def print_state_point(label: str, dry_bulb_f: float,
                       relative_humidity_pct: float, altitude_ft: float = 0) -> None:
    """Print a full psychrometric state point."""
    w = humidity_ratio(dry_bulb_f, relative_humidity_pct, altitude_ft)
    h = enthalpy_btu_per_lb(dry_bulb_f, relative_humidity_pct, altitude_ft)
    dp = dew_point_f(dry_bulb_f, relative_humidity_pct)
    wb = wet_bulb_f(dry_bulb_f, relative_humidity_pct, altitude_ft)
    print(f"\n{'='*50}")
    print(f"State Point: {label}")
    print(f"{'='*50}")
    print(f"  Dry Bulb        : {dry_bulb_f:.1f} °F")
    print(f"  Wet Bulb        : {wb:.1f} °F")
    print(f"  Dew Point       : {dp:.1f} °F")
    print(f"  Relative Humid  : {relative_humidity_pct:.1f} %")
    print(f"  Humidity Ratio  : {w:.5f} lb/lb")
    print(f"  Enthalpy        : {h:.2f} BTU/lb")
