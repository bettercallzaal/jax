"""
ASHRAE standards quick-reference and calculation helpers.
ASHRAE 55 (Comfort), 62.1 (Ventilation), 90.1 (Energy).
"""


# ---------------------------------------------------------------------------
# ASHRAE 62.1 — Ventilation for Indoor Air Quality
# ---------------------------------------------------------------------------

# People-component (CFM/person) and area-component (CFM/ft²) per occupancy type
# Source: ASHRAE 62.1-2019 Table 6.2.2.1
VENTILATION_RATES = {
    "office":              {"cfm_per_person": 5,  "cfm_per_sqft": 0.06, "default_density_per_1000sqft": 5},
    "conference":          {"cfm_per_person": 5,  "cfm_per_sqft": 0.06, "default_density_per_1000sqft": 50},
    "reception":           {"cfm_per_person": 5,  "cfm_per_sqft": 0.06, "default_density_per_1000sqft": 30},
    "lobby":               {"cfm_per_person": 7.5,"cfm_per_sqft": 0.06, "default_density_per_1000sqft": 10},
    "classroom":           {"cfm_per_person": 10, "cfm_per_sqft": 0.12, "default_density_per_1000sqft": 35},
    "lab_general":         {"cfm_per_person": 10, "cfm_per_sqft": 0.18, "default_density_per_1000sqft": 25},
    "lab_bio_bsl2":        {"cfm_per_person": 10, "cfm_per_sqft": 1.0,  "default_density_per_1000sqft": 25},
    "animal_room":         {"cfm_per_person": 10, "cfm_per_sqft": 0.18, "default_density_per_1000sqft": 10},
    "hospital_patient":    {"cfm_per_person": 25, "cfm_per_sqft": 0.06, "default_density_per_1000sqft": 10},
    "corridor":            {"cfm_per_person": 0,  "cfm_per_sqft": 0.06, "default_density_per_1000sqft": 0},
    "restroom":            {"cfm_per_person": 0,  "cfm_per_sqft": 0.18, "default_density_per_1000sqft": 0},
    "retail":              {"cfm_per_person": 7.5,"cfm_per_sqft": 0.12, "default_density_per_1000sqft": 15},
    "gym":                 {"cfm_per_person": 20, "cfm_per_sqft": 0.18, "default_density_per_1000sqft": 10},
    "parking_garage":      {"cfm_per_person": 0,  "cfm_per_sqft": 0.75, "default_density_per_1000sqft": 0},
    "kitchen_commercial":  {"cfm_per_person": 7.5,"cfm_per_sqft": 0.18, "default_density_per_1000sqft": 20},
    "warehouse":           {"cfm_per_person": 10, "cfm_per_sqft": 0.06, "default_density_per_1000sqft": 2},
}

CO2_OUTDOOR_BASELINE_PPM = 420  # 2024 value
CO2_COMFORT_LIMIT_PPM = 1100    # ASHRAE 62.1 indicator of 1000 ppm above outdoor
CO2_ALARM_PPM = 5000            # OSHA 8-hr PEL


def min_outdoor_air_cfm(
    occupancy_type: str,
    floor_area_sqft: float,
    occupants: int,
    ventilation_effectiveness: float = 1.0,
) -> dict:
    """Calculate minimum outdoor air per ASHRAE 62.1 Ventilation Rate Procedure."""
    data = VENTILATION_RATES.get(occupancy_type.lower())
    if not data:
        available = list(VENTILATION_RATES.keys())
        raise ValueError(f"Unknown occupancy type '{occupancy_type}'. Available: {available}")

    rp = data["cfm_per_person"] * occupants
    ra = data["cfm_per_sqft"] * floor_area_sqft
    vbz = rp + ra  # breathing zone OA flow
    voz = vbz / ventilation_effectiveness  # zone OA flow

    return {
        "occupancy_type": occupancy_type,
        "occupants": occupants,
        "floor_area_sqft": floor_area_sqft,
        "people_component_cfm": round(rp, 1),
        "area_component_cfm": round(ra, 1),
        "breathing_zone_cfm": round(vbz, 1),
        "zone_outdoor_air_cfm": round(voz, 1),
        "cfm_per_person_total": round(voz / occupants, 1) if occupants else None,
        "note": "Per ASHRAE 62.1-2019 Table 6.2.2.1",
    }


def co2_based_occupancy_estimate(co2_ppm: float, cfm_per_person: float = 15.0,
                                  outdoor_co2_ppm: float = CO2_OUTDOOR_BASELINE_PPM) -> int:
    """Rough occupancy estimate from CO2 level (DCV logic)."""
    if co2_ppm <= outdoor_co2_ppm:
        return 0
    # Each person generates ~0.3 L/min CO2 → simplified mass balance
    # N_people ≈ (Vzone × ΔCO2/ppm_per_person) but simplified:
    # Assumes 0.3 CFM generation per person, steady state
    delta_ppm = co2_ppm - outdoor_co2_ppm
    gen_cfm_per_person = 0.30  # rough adult activity
    oa_cfm = cfm_per_person
    # Steady-state: N × gen = (ppm_rise/10^6) × oa_cfm_total
    # ppm_rise × oa_total / (10^6 × gen_per_person) ≈ N
    est = int(delta_ppm * oa_cfm / (1e6 * gen_cfm_per_person / 1000))
    return max(0, est)


# ---------------------------------------------------------------------------
# ASHRAE 55 — Thermal Comfort
# ---------------------------------------------------------------------------

COMFORT_ZONES = {
    "summer": {"t_min_f": 74, "t_max_f": 80, "rh_max_pct": 60, "rh_min_pct": 30},
    "winter": {"t_min_f": 68, "t_max_f": 74, "rh_max_pct": 60, "rh_min_pct": 30},
}

ASHRAE55_AIR_VELOCITY_MAX_FPM = 30  # 0.15 m/s max in occupied zone for no draft


def comfort_assessment(
    room_temp_f: float,
    relative_humidity_pct: float,
    season: str = "winter",
    air_velocity_fpm: float = 20,
) -> dict:
    """Assess comfort against ASHRAE 55 criteria."""
    zone = COMFORT_ZONES.get(season.lower(), COMFORT_ZONES["winter"])
    issues = []

    temp_ok = zone["t_min_f"] <= room_temp_f <= zone["t_max_f"]
    rh_ok = zone["rh_min_pct"] <= relative_humidity_pct <= zone["rh_max_pct"]
    velocity_ok = air_velocity_fpm <= ASHRAE55_AIR_VELOCITY_MAX_FPM

    if not temp_ok:
        direction = "too warm" if room_temp_f > zone["t_max_f"] else "too cold"
        issues.append(f"Temperature {room_temp_f:.1f}°F is {direction} (ASHRAE 55 {season}: {zone['t_min_f']}–{zone['t_max_f']}°F)")
    if not rh_ok:
        direction = "too humid" if relative_humidity_pct > zone["rh_max_pct"] else "too dry"
        issues.append(f"Humidity {relative_humidity_pct:.0f}% RH is {direction} (ASHRAE 55: 30–60% RH)")
    if not velocity_ok:
        issues.append(f"Air velocity {air_velocity_fpm:.0f} fpm exceeds {ASHRAE55_AIR_VELOCITY_MAX_FPM} fpm (draft complaint likely)")

    return {
        "season": season,
        "temp_f": room_temp_f,
        "rh_pct": relative_humidity_pct,
        "velocity_fpm": air_velocity_fpm,
        "in_comfort_zone": temp_ok and rh_ok and velocity_ok,
        "temperature_ok": temp_ok,
        "humidity_ok": rh_ok,
        "velocity_ok": velocity_ok,
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# ASHRAE 90.1 — Energy Efficiency
# ---------------------------------------------------------------------------

def supply_air_temp_reset(
    zone_temp_f: float,
    zone_setpoint_f: float = 72,
    base_sat_f: float = 55,
    max_sat_f: float = 62,
) -> float:
    """
    ASHRAE 90.1 supply air temperature reset.
    Raise SAT when zone is below setpoint to save cooling energy.
    Returns target supply air temperature.
    """
    offset = zone_setpoint_f - zone_temp_f  # positive = zone is cold
    # 1°F reset per 5°F zone temperature offset below setpoint
    reset = max(0, offset / 5)
    return min(max_sat_f, base_sat_f + reset)


def economizer_enabled(
    outdoor_enthalpy_btu_lb: float,
    return_enthalpy_btu_lb: float,
    outdoor_temp_f: float = None,
    lockout_temp_f: float = 75,
) -> bool:
    """
    Determine if economizer should be enabled (enthalpy-based).
    ASHRAE 90.1: Use economizer when OA enthalpy < return enthalpy.
    """
    enthalpy_ok = outdoor_enthalpy_btu_lb < return_enthalpy_btu_lb
    if outdoor_temp_f is not None:
        temp_ok = outdoor_temp_f < lockout_temp_f
        return enthalpy_ok and temp_ok
    return enthalpy_ok


def chilled_water_reset(
    return_water_temp_f: float,
    base_cwst_f: float = 44,
    max_cwst_f: float = 54,
) -> float:
    """
    ASHRAE 90.1 chilled water supply temperature reset.
    Raise CWST 1°F per 2°F rise in return water temp.
    """
    offset = max(0, return_water_temp_f - 54)  # 54°F baseline return
    reset = offset / 2
    return min(max_cwst_f, base_cwst_f + reset)


def print_ventilation_report(result: dict) -> None:
    print(f"\n{'='*50}")
    print(f"ASHRAE 62.1 VENTILATION REQUIREMENT")
    print(f"{'='*50}")
    print(f"  Space           : {result['occupancy_type']}")
    print(f"  Floor Area      : {result['floor_area_sqft']:,.0f} ft²")
    print(f"  Occupants       : {result['occupants']}")
    print(f"  People Comp.    : {result['people_component_cfm']:.0f} CFM")
    print(f"  Area Comp.      : {result['area_component_cfm']:.0f} CFM")
    print(f"  Min OA Required : {result['zone_outdoor_air_cfm']:.0f} CFM")
    if result["cfm_per_person_total"]:
        print(f"  Per Person      : {result['cfm_per_person_total']:.1f} CFM/person")
    print(f"  {result['note']}")


def print_comfort_report(result: dict) -> None:
    status = "COMFORTABLE" if result["in_comfort_zone"] else "OUT OF COMFORT ZONE"
    print(f"\n{'='*50}")
    print(f"ASHRAE 55 COMFORT ASSESSMENT — {result['season'].upper()}")
    print(f"Status: {status}")
    print(f"{'='*50}")
    print(f"  Temperature : {result['temp_f']:.1f}°F  {'✓' if result['temperature_ok'] else '✗'}")
    print(f"  Humidity    : {result['rh_pct']:.0f}% RH  {'✓' if result['humidity_ok'] else '✗'}")
    print(f"  Air Velocity: {result['velocity_fpm']:.0f} fpm  {'✓' if result['velocity_ok'] else '✗'}")
    if result["issues"]:
        print("\n  Issues:")
        for issue in result["issues"]:
            print(f"    • {issue}")
